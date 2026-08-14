"""
VESUVIUS RITE OF PASSAGE — 2.5D U-Net ink-detection baseline.

Purpose: produce YOUR first ink image from real fragment data. This teaches
you the terrain (surface volumes, masks, labels, patches, inference
stitching). It is practice — NOT an August submission.

WHERE TO RUN:
  Kaggle notebook with free GPU:
    1. kaggle.com -> New Notebook -> Settings -> Accelerator: GPU
    2. "Add Input" -> search dataset: vesuvius-challenge-ink-detection
    3. Upload this file or paste it into a cell, then:  %run train_ink_baseline.py
  (Any machine with the data + a GPU also works; edit CFG["data_dir"].)

WHAT SUCCESS LOOKS LIKE:
  out/prediction.png shows ghostly bright strokes where the model believes
  ink is, on a region it never trained on. Compare with out/ground_truth.png.

Dependencies: torch, numpy, pillow (all preinstalled on Kaggle).
"""

import os
import random
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # fragments are huge; disable PIL's bomb check

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

try:
    from tqdm import tqdm
except ImportError:  # tqdm is nice, not required
    def tqdm(x, **k):
        return x

# ----------------------------------------------------------------------------
# CONFIG — the only block you should need to touch
# ----------------------------------------------------------------------------
CFG = {
    # Kaggle mounts competition data at one of two places depending on the
    # kernel's docker image: the classic path, or under competitions/ on the
    # byod images. Detect it so the same file runs unmodified in both.
    "data_dir": next(
        (p for p in [
            "/kaggle/input/vesuvius-challenge-ink-detection/train",
            "/kaggle/input/competitions/vesuvius-challenge-ink-detection/train",
        ] if os.path.isdir(p)),
        "/kaggle/input/vesuvius-challenge-ink-detection/train",
    ),
    "fragment": "1",     # "1" is the classic starter fragment
    "z_start": 24,       # the middle slices carry most of the ink signal
    "z_dim": 16,         # how many slices the model sees (input channels)
    "patch": 224,        # training patch size (pixels)
    "stride": 112,       # patch grid stride (overlapping patches)
    "batch_size": 16,
    "epochs": 8,
    "lr": 1e-4,
    "val_frac": 0.15,    # rightmost vertical strip is held out for validation
    "mask_min": 0.05,    # keep patches with at least this much papyrus
    "out_dir": "out",
    "seed": 42,
}

# ----------------------------------------------------------------------------
# Reproducibility + device
# ----------------------------------------------------------------------------
random.seed(CFG["seed"])
np.random.seed(CFG["seed"])
torch.manual_seed(CFG["seed"])

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
if DEVICE == "cpu":
    print("WARNING: no GPU found — this will be painfully slow. "
          "On Kaggle: Settings -> Accelerator -> GPU.")


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
def load_fragment(frag_dir, z_start, z_dim):
    """Return (volume[z,H,W] float16 in 0..1, mask[H,W] bool, labels[H,W] float32)."""
    mask = np.array(Image.open(os.path.join(frag_dir, "mask.png")).convert("L")) > 0
    labels = (np.array(Image.open(os.path.join(frag_dir, "inklabels.png")).convert("L")) > 0)
    labels = labels.astype(np.float32)

    slices = []
    for z in tqdm(range(z_start, z_start + z_dim), desc="loading slices"):
        p = os.path.join(frag_dir, "surface_volume", f"{z:02}.tif")
        arr = np.array(Image.open(p), dtype=np.float32) / 65535.0
        slices.append(arr.astype(np.float16))  # float16 to fit in RAM
    volume = np.stack(slices)  # (z_dim, H, W)
    return volume, mask, labels


def build_patch_grid(mask, patch, stride, mask_min):
    """All (y, x) top-left corners whose patch contains enough papyrus."""
    H, W = mask.shape
    coords = []
    for y in range(0, H - patch + 1, stride):
        for x in range(0, W - patch + 1, stride):
            if mask[y:y + patch, x:x + patch].mean() >= mask_min:
                coords.append((y, x))
    return coords


class PatchDataset(Dataset):
    def __init__(self, volume, labels, coords, patch, augment):
        self.volume, self.labels = volume, labels
        self.coords, self.patch, self.augment = coords, patch, augment

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, i):
        y, x = self.coords[i]
        p = self.patch
        img = self.volume[:, y:y + p, x:x + p].astype(np.float32)   # (C,H,W)
        lab = self.labels[y:y + p, x:x + p][None]                    # (1,H,W)
        if self.augment:
            k = random.randint(0, 3)
            if k:
                img = np.rot90(img, k, axes=(1, 2))
                lab = np.rot90(lab, k, axes=(1, 2))
            if random.random() < 0.5:
                img = np.flip(img, axis=2)
                lab = np.flip(lab, axis=2)
        return torch.from_numpy(img.copy()), torch.from_numpy(lab.copy())


# ----------------------------------------------------------------------------
# Model — a compact U-Net (input channels = z_dim slices, output = ink logit)
# ----------------------------------------------------------------------------
class DoubleConv(nn.Module):
    def __init__(self, c_in, c_out):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(c_in, c_out, 3, padding=1, bias=False),
            nn.BatchNorm2d(c_out), nn.ReLU(inplace=True),
            nn.Conv2d(c_out, c_out, 3, padding=1, bias=False),
            nn.BatchNorm2d(c_out), nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.block(x)


class UNet(nn.Module):
    def __init__(self, c_in, base=32):
        super().__init__()
        self.d1 = DoubleConv(c_in, base)
        self.d2 = DoubleConv(base, base * 2)
        self.d3 = DoubleConv(base * 2, base * 4)
        self.d4 = DoubleConv(base * 4, base * 8)
        self.pool = nn.MaxPool2d(2)
        self.up3 = nn.ConvTranspose2d(base * 8, base * 4, 2, stride=2)
        self.u3 = DoubleConv(base * 8, base * 4)
        self.up2 = nn.ConvTranspose2d(base * 4, base * 2, 2, stride=2)
        self.u2 = DoubleConv(base * 4, base * 2)
        self.up1 = nn.ConvTranspose2d(base * 2, base, 2, stride=2)
        self.u1 = DoubleConv(base * 2, base)
        self.head = nn.Conv2d(base, 1, 1)

    def forward(self, x):
        s1 = self.d1(x)
        s2 = self.d2(self.pool(s1))
        s3 = self.d3(self.pool(s2))
        b = self.d4(self.pool(s3))
        x = self.u3(torch.cat([self.up3(b), s3], dim=1))
        x = self.u2(torch.cat([self.up2(x), s2], dim=1))
        x = self.u1(torch.cat([self.up1(x), s1], dim=1))
        return self.head(x)


def dice_score(logits, target, eps=1e-6):
    prob = torch.sigmoid(logits)
    pred = (prob > 0.5).float()
    inter = (pred * target).sum()
    return ((2 * inter + eps) / (pred.sum() + target.sum() + eps)).item()


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    os.makedirs(CFG["out_dir"], exist_ok=True)
    frag_dir = os.path.join(CFG["data_dir"], CFG["fragment"])

    volume, mask, labels = load_fragment(frag_dir, CFG["z_start"], CFG["z_dim"])
    H, W = mask.shape
    split_x = int(W * (1 - CFG["val_frac"]))  # right strip = validation
    print(f"fragment {CFG['fragment']}: {H}x{W}, validation strip starts at x={split_x}")

    coords = build_patch_grid(mask, CFG["patch"], CFG["stride"], CFG["mask_min"])
    train_c = [c for c in coords if c[1] + CFG["patch"] <= split_x]
    val_c = [c for c in coords if c[1] >= split_x]
    print(f"patches: {len(train_c)} train / {len(val_c)} val")

    train_dl = DataLoader(PatchDataset(volume, labels, train_c, CFG["patch"], True),
                          batch_size=CFG["batch_size"], shuffle=True,
                          num_workers=2, pin_memory=True, drop_last=True)
    val_dl = DataLoader(PatchDataset(volume, labels, val_c, CFG["patch"], False),
                        batch_size=CFG["batch_size"], shuffle=False,
                        num_workers=2, pin_memory=True)

    model = UNet(CFG["z_dim"]).to(DEVICE)
    opt = torch.optim.AdamW(model.parameters(), lr=CFG["lr"])
    loss_fn = nn.BCEWithLogitsLoss()
    scaler = torch.cuda.amp.GradScaler(enabled=(DEVICE == "cuda"))

    best_dice = 0.0
    for epoch in range(1, CFG["epochs"] + 1):
        model.train()
        tr_loss = 0.0
        for img, lab in tqdm(train_dl, desc=f"epoch {epoch} train"):
            img, lab = img.to(DEVICE), lab.to(DEVICE)
            opt.zero_grad(set_to_none=True)
            with torch.cuda.amp.autocast(enabled=(DEVICE == "cuda")):
                loss = loss_fn(model(img), lab)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
            tr_loss += loss.item()

        model.eval()
        va_loss, va_dice, n = 0.0, 0.0, 0
        with torch.no_grad():
            for img, lab in val_dl:
                img, lab = img.to(DEVICE), lab.to(DEVICE)
                logits = model(img)
                va_loss += loss_fn(logits, lab).item()
                va_dice += dice_score(logits, lab)
                n += 1
        va_loss, va_dice = va_loss / max(n, 1), va_dice / max(n, 1)
        print(f"epoch {epoch}: train_loss={tr_loss/len(train_dl):.4f} "
              f"val_loss={va_loss:.4f} val_dice={va_dice:.4f}")
        if va_dice > best_dice:
            best_dice = va_dice
            torch.save(model.state_dict(), os.path.join(CFG["out_dir"], "best.pt"))
            print(f"  ^ new best (dice {best_dice:.4f}) — saved")

    # ------------------------------------------------------------------
    # Inference: sliding window over the validation strip -> ink image
    # ------------------------------------------------------------------
    print("running sliding-window inference on the validation strip...")
    model.load_state_dict(torch.load(os.path.join(CFG["out_dir"], "best.pt")))
    model.eval()
    p, s = CFG["patch"], CFG["stride"]
    acc = np.zeros((H, W - split_x), dtype=np.float32)
    cnt = np.zeros_like(acc)
    with torch.no_grad():
        for y in tqdm(range(0, H - p + 1, s), desc="inference"):
            batch, spots = [], []
            for x in range(split_x, W - p + 1, s):
                batch.append(volume[:, y:y + p, x:x + p].astype(np.float32))
                spots.append(x - split_x)
            if not batch:
                continue
            t = torch.from_numpy(np.stack(batch)).to(DEVICE)
            with torch.cuda.amp.autocast(enabled=(DEVICE == "cuda")):
                prob = torch.sigmoid(model(t)).squeeze(1).float().cpu().numpy()
            for pr, x0 in zip(prob, spots):
                acc[y:y + p, x0:x0 + p] += pr
                cnt[y:y + p, x0:x0 + p] += 1

    pred = np.divide(acc, cnt, out=np.zeros_like(acc), where=cnt > 0)
    pred *= mask[:, split_x:]  # blank out non-papyrus
    Image.fromarray((pred * 255).astype(np.uint8)).save(
        os.path.join(CFG["out_dir"], "prediction.png"))
    Image.fromarray((labels[:, split_x:] * 255).astype(np.uint8)).save(
        os.path.join(CFG["out_dir"], "ground_truth.png"))
    print(f"DONE. Open {CFG['out_dir']}/prediction.png — those bright strokes "
          "are 2,000-year-old ink, found by YOUR model. Post it.")


if __name__ == "__main__":
    main()
