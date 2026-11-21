"""Diagnose a talking-head video against its source picture and audio, with face tracking.

v2 tracks the face from frame to frame (position and zoom, by template matching
against the source picture), so the mouth box follows the face even when the
model moves the camera or the head. v1 used fixed boxes, which OmniHuman's
moving shots defeated.

Runs in the ElevenLabs sandbox (offline; ffmpeg, numpy, pillow).
Usage:
  python3 diagnose_video_v2.py VIDEO SOURCE_IMAGE SOURCE_AUDIO LABEL FACE MOUTH
FACE and MOUTH are boxes as fractions of the source picture: "x0,y0,x1,y1".
Prints one compact JSON object (the sandbox only returns ~6k characters).
"""
import json
import subprocess
import sys

import numpy as np
from PIL import Image

VIDEO, SRC_IMG, SRC_AUDIO, LABEL, FACE, MOUTH = sys.argv[1:7]
FACE = [float(v) for v in FACE.split(",")]
MOUTH = [float(v) for v in MOUTH.split(",")]
FPS, W, H = 25, 320, 180
SCALES = (0.8, 0.9, 1.0, 1.1, 1.25, 1.4, 1.6)
MW, MH = 40, 20          # mouth patch size after resampling


def run(cmd):
    return subprocess.run(cmd, capture_output=True, check=True).stdout


def probe(path):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "stream=codec_type,width,height,r_frame_rate:format=duration,size",
               "-of", "json", path])
    return json.loads(out)


def frames(path):
    raw = run(["ffmpeg", "-v", "error", "-i", path, "-vf",
               f"fps={FPS},scale={W}:{H},format=gray", "-f", "rawvideo", "-"])
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)


def pcm(path, sr=16000):
    raw = run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr),
               "-f", "f32le", "-"])
    return np.frombuffer(raw, np.float32), sr


def corr(a, b):
    a = (a - a.mean()) / (a.std() + 1e-9)
    b = (b - b.mean()) / (b.std() + 1e-9)
    return float((a * b).mean())


def lag_search(sig, ref, max_lag=8):
    best = (0, -9.0)
    for lag in range(-max_lag, max_lag + 1):
        a = sig[lag:] if lag >= 0 else sig[:lag]
        b = ref[:len(ref) - lag] if lag >= 0 else ref[-lag:]
        k = min(len(a), len(b))
        r = corr(a[:k], b[:k])
        if r > best[1]:
            best = (lag, r)
    return best


def ncc_map(frame, tmpl):
    """Normalised cross-correlation of tmpl over frame (valid positions), via FFT."""
    th, tw = tmpl.shape
    t = tmpl - tmpl.mean()
    tn = np.sqrt((t ** 2).sum()) + 1e-9
    fh, fw = frame.shape
    shape = (fh + th, fw + tw)
    num = np.fft.irfft2(np.fft.rfft2(frame, shape) * np.conj(np.fft.rfft2(t, shape)), shape)
    num = num[:fh - th + 1, :fw - tw + 1]
    # local sums for the frame std under the template window (integral images)
    ii = np.pad(frame, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    ii2 = np.pad(frame ** 2, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    def win(s):
        return s[th:, tw:] - s[:-th, tw:] - s[th:, :-tw] + s[:-th, :-tw]
    n = th * tw
    s1, s2 = win(ii), win(ii2)
    var = np.maximum(s2 - s1 ** 2 / n, 1e-6)
    return num / (np.sqrt(var) * tn)


# --- source picture and face template -------------------------------------
src = np.asarray(Image.open(SRC_IMG).convert("L").resize((W, H)), np.float32)
fx0, fy0, fx1, fy1 = int(FACE[0] * W), int(FACE[1] * H), int(FACE[2] * W), int(FACE[3] * H)
face_t = src[fy0:fy1, fx0:fx1]
tmpls = {}
for s in SCALES:
    tw, th = max(8, int(face_t.shape[1] * s)), max(8, int(face_t.shape[0] * s))
    if tw < W and th < H:
        tmpls[s] = np.asarray(Image.fromarray(face_t).resize((tw, th)), np.float32)

# mouth box relative to the face box (fractions of the face box)
rel = ((MOUTH[0] - FACE[0]) / (FACE[2] - FACE[0]), (MOUTH[1] - FACE[1]) / (FACE[3] - FACE[1]),
       (MOUTH[2] - FACE[0]) / (FACE[2] - FACE[0]), (MOUTH[3] - FACE[1]) / (FACE[3] - FACE[1]))

# --- video -----------------------------------------------------------------
info = probe(VIDEO)
vs = next(s for s in info["streams"] if s["codec_type"] == "video")
has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
num_, den_ = vs["r_frame_rate"].split("/")
dur = float(info["format"]["duration"])
a_src, sr = pcm(SRC_AUDIO)
F = frames(VIDEO)

y, sr = pcm(VIDEO if has_audio else SRC_AUDIO)
hop = sr // FPS
nf = len(y) // hop
rms = np.sqrt((y[:nf * hop].reshape(nf, hop) ** 2).mean(axis=1))
m = min(len(F), len(rms))
F, rms = F[:m], rms[:m]
speech = rms > 0.15 * rms.max()

# --- track the face in every frame -----------------------------------------
track = []          # (conf, x, y, scale)
for f in F:
    best = (-9.0, 0, 0, 1.0)
    for s, t in tmpls.items():
        mp = ncc_map(f, t)
        i = int(np.argmax(mp))
        yy, xx = divmod(i, mp.shape[1])
        if mp.flat[i] > best[0]:
            best = (float(mp.flat[i]), xx, yy, s)
    track.append(best)
conf = np.array([t[0] for t in track])
xs = np.array([t[1] for t in track], float)
ys = np.array([t[2] for t in track], float)
sc = np.array([t[3] for t in track], float)

# mouth patch at the tracked position
patches = []
for f, (c, x, y0, s) in zip(F, track):
    fw, fh = (fx1 - fx0) * s, (fy1 - fy0) * s
    mx0, my0 = x + rel[0] * fw, y0 + rel[1] * fh
    mx1, my1 = x + rel[2] * fw, y0 + rel[3] * fh
    box = (max(0, int(mx0)), max(0, int(my0)), min(W, max(int(mx0) + 2, int(mx1))), min(H, max(int(my0) + 2, int(my1))))
    patches.append(np.asarray(Image.fromarray(f).crop(box).resize((MW, MH)), np.float32))
P = np.stack(patches)
rest = np.median(P[~speech] if (~speech).sum() > 5 else P, axis=0)
dev = np.abs(P - rest).mean(axis=(1, 2))
motion = np.abs(np.diff(P, axis=0)).mean(axis=(1, 2))
dev_lag, dev_r = lag_search(dev, rms)
on_lag, on_r = lag_search(motion, np.abs(np.diff(rms)))
sp = speech[1:]
still = float(motion[~sp].mean() / motion[sp].mean()) if sp.any() and (~sp).any() else None

# --- framing and lighting timeline (1 s steps) ------------------------------
ident = [corr(F[i], src) for i in range(0, m, FPS)]
bright = [float(F[i].mean()) for i in range(0, m, FPS)]

# background: pixels outside the tracked face box, frame-to-frame change
bg = []
for i in range(1, m):
    mask = np.ones((H, W), bool)
    c, x, y0, s = track[i]
    mask[int(y0):int(y0 + (fy1 - fy0) * s), int(x):int(x + (fx1 - fx0) * s)] = False
    bg.append(float(np.abs(F[i] - F[i - 1])[mask].mean()))
face_move = float(np.hypot(np.diff(xs), np.diff(ys)).mean())

print(json.dumps({
    "label": LABEL,
    "size": f'{vs["width"]}x{vs["height"]}',
    "fps": round(int(num_) / int(den_), 2),
    "dur_s": round(dur, 2), "audio_s": round(len(a_src) / sr, 2),
    "mb": round(int(info["format"]["size"]) / 1e6, 2),
    "track_conf_median": round(float(np.median(conf)), 3),
    "track_conf_p10": round(float(np.percentile(conf, 10)), 3),
    "face_shift_px_per_frame": round(face_move, 2),
    "face_x_range_pct": round(float((xs.max() - xs.min()) / W * 100), 1),
    "face_y_range_pct": round(float((ys.max() - ys.min()) / H * 100), 1),
    "zoom_range": [float(sc.min()), float(sc.max())],
    "lipsync_r": round(dev_r, 3), "lipsync_lag_ms": dev_lag * 1000 // FPS,
    "onset_r": round(on_r, 3),
    "still_ratio": round(still, 3) if still is not None else None,
    "mouth_activity": round(float(dev[speech].mean()), 2),
    "bg_motion": round(float(np.mean(bg)), 3),
    "ident_1s": [round(v, 2) for v in ident],
    "bright_1s": [round(v) for v in bright],
}))
