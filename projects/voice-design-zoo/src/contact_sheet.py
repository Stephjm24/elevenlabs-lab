"""Contact sheet for talking-head videos: one row per video.

Each row: frames at 5%, 50% and 95% of the clip, then close-ups of the
mouth at the loudest moment and at the quietest moment mid-clip.
Usage: python3 contact_sheet.py OUT.jpg LABEL1=VIDEO1 [LABEL2=VIDEO2 ...]
"""
import io
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

FW, FH = 240, 135          # full-frame thumbnail
MW = 135                   # mouth close-up (square)
MOUTH = (0.40, 0.33, 0.60, 0.62)   # crop for the close-up, as fractions


def grab(path, t):
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path,
                          "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(png)).convert("RGB")


def envelope(path, fps=25, sr=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr),
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    y = np.frombuffer(raw, np.float32)
    hop = sr // fps
    n = len(y) // hop
    return np.sqrt((y[:n * hop].reshape(n, hop) ** 2).mean(axis=1)), fps


out = sys.argv[1]
rows = [a.split("=", 1) for a in sys.argv[2:]]
LABEL_W = 90
sheet = Image.new("RGB", (LABEL_W + 3 * FW + 2 * MW + 6 * 4, len(rows) * (FH + 4) + 18), "white")
d = ImageDraw.Draw(sheet)
heads = [("5%", FW), ("50%", FW), ("95%", FW), ("mouth: loudest", MW), ("mouth: pause", MW)]
hx = LABEL_W
for text, w in heads:
    d.text((hx + 2, 3), text, fill="black")
    hx += w + 4
for r, (label, path) in enumerate(rows):
    y0 = 18 + r * (FH + 4)
    env, fps = envelope(path)
    dur = len(env) / fps
    d.text((4, y0 + FH // 2 - 6), label, fill="black")
    x = LABEL_W
    for frac in (0.05, 0.5, 0.95):
        sheet.paste(grab(path, frac * dur).resize((FW, FH)), (x, y0))
        x += FW + 4
    mid = slice(int(0.1 * len(env)), int(0.9 * len(env)))
    loud = int(np.argmax(env)) / fps
    quiet = (int(np.argmin(env[mid])) + mid.start) / fps
    for t in (loud, quiet):
        img = grab(path, t)
        w, h = img.size
        x0, y0f, x1, y1 = MOUTH
        crop = img.crop((int(x0 * w), int(y0f * h), int(x1 * w), int(y1 * h))).resize((MW, FH))
        sheet.paste(crop, (x, y0))
        x += MW + 4
sheet.save(out, quality=62)
print(out, sheet.size)
