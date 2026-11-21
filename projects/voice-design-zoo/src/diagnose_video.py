"""Diagnose a talking-head video against its source picture and audio.

Runs inside the ElevenLabs sandbox (offline; ffmpeg, numpy, librosa, pillow).
Usage: python3 diagnose_video.py VIDEO SOURCE_IMAGE SOURCE_AUDIO LABEL
Prints one JSON object.

Regions are fractions of the frame, measured on the source picture
(lighthouse keeper: face centred, mouth at about x=0.50, y=0.47).
They only line up when the output keeps the picture's framing, so the
script reports the output's aspect ratio next to them.
"""
import json
import subprocess
import sys

import librosa
import numpy as np
from PIL import Image

VIDEO, SRC_IMG, SRC_AUDIO, LABEL = sys.argv[1:5]
FPS = 25            # analysis frame rate
W, H = 320, 180     # analysis size (16:9)

REGIONS = {         # (x0, y0, x1, y1) as fractions of the frame
    "mouth": (0.44, 0.40, 0.57, 0.55),
    "face": (0.33, 0.05, 0.64, 0.62),
    "bg_window": (0.04, 0.10, 0.26, 0.45),
    "bg_lamp": (0.76, 0.05, 0.95, 0.55),
}


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,codec_name,width,height,r_frame_rate:format=duration,bit_rate,size",
         "-of", "json", path], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def frames(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={FPS},scale={W}:{H},format=gray",
         "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)


def box(arr, name):
    x0, y0, x1, y1 = REGIONS[name]
    return arr[..., int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)]


def pcm(path, sr=16000):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32), sr


def corr(a, b):
    a = (a - a.mean()) / (a.std() + 1e-9)
    b = (b - b.mean()) / (b.std() + 1e-9)
    return float((a * b).mean())


info = probe(VIDEO)
vs = next(s for s in info["streams"] if s["codec_type"] == "video")
has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
num, den = vs["r_frame_rate"].split("/")
dur = float(info["format"]["duration"])
_a, _sr = pcm(SRC_AUDIO)
src_dur = len(_a) / _sr

F = frames(VIDEO)
n = len(F)

# Audio envelope at the analysis frame rate (from the video's own track if it has one).
y, sr = pcm(VIDEO if has_audio else SRC_AUDIO)
hop = sr // FPS
rms = librosa.feature.rms(y=y, frame_length=hop * 2, hop_length=hop)[0]
m = min(n, len(rms))
rms, F = rms[:m], F[:m]
speech = rms > (0.15 * rms.max())          # frames where he is talking

# Mouth: motion (frame-to-frame change) and darkness (open mouths are darker).
mouth = box(F, "mouth")
mouth_motion = np.abs(np.diff(mouth, axis=0)).mean(axis=(1, 2))
mouth_dark = -mouth.mean(axis=(1, 2))
# Deviation from the resting mouth (works whether opening shows dark gaps or bright teeth).
rest = np.median(mouth[~speech] if (~speech).sum() > 5 else mouth, axis=0)
mouth_dev = np.abs(mouth - rest).mean(axis=(1, 2))

def lag_search(sig, ref, max_lag=8):
    """Best correlation of sig against ref within +-max_lag frames (+lag = video late)."""
    best = (0, -9.0)
    for lag in range(-max_lag, max_lag + 1):
        a = sig[lag:] if lag >= 0 else sig[:lag]
        b = ref[:len(ref) - lag] if lag >= 0 else ref[-lag:]
        k = min(len(a), len(b))
        r = corr(a[:k], b[:k])
        if r > best[1]:
            best = (lag, r)
    return best


# Main score: mouth darkness follows loudness (open when loud, closed when quiet).
open_lag, open_r = lag_search(mouth_dark[:m], rms)
dev_lag, dev_r = lag_search(mouth_dev[:m], rms)
# Secondary: mouth movement follows *changes* in loudness (syllable onsets).
move_lag, move_r = lag_search(mouth_motion, np.abs(np.diff(rms)))

sp = speech[1:]
motion_speech = float(mouth_motion[sp].mean()) if sp.any() else None
motion_silence = float(mouth_motion[~sp].mean()) if (~sp).any() else None

# Liveliness and stability.
face_motion = float(np.abs(np.diff(box(F, "face"), axis=0)).mean())
bg_motion = float(np.mean([np.abs(np.diff(box(F, k), axis=0)).mean() for k in ("bg_window", "bg_lamp")]))

# Identity drift: face region vs the source picture at start, middle and end.
src = np.asarray(Image.open(SRC_IMG).convert("L").resize((W, H)), np.float32)
src_face = box(src, "face")
drift = {}
for name, idx in (("start", 0), ("middle", m // 2), ("end", m - 1)):
    drift[name] = round(corr(box(F[idx], "face").ravel(), src_face.ravel()), 3)

print(json.dumps({
    "label": LABEL,
    "width": vs["width"], "height": vs["height"],
    "aspect": round(vs["width"] / vs["height"], 3),
    "fps": round(int(num) / int(den), 2),
    "codec": vs["codec_name"],
    "has_audio": has_audio,
    "duration_s": round(dur, 2),
    "source_audio_s": round(src_dur, 2),
    "duration_delta_s": round(dur - src_dur, 2),
    "file_mb": round(int(info["format"]["size"]) / 1e6, 2),
    "bitrate_kbps": round(int(info["format"].get("bit_rate", 0)) / 1000),
    "lipsync_r_dev": round(dev_r, 3),
    "lipsync_lag_ms": dev_lag * 1000 // FPS,
    "lipsync_r_dark": round(open_r, 3),
    "lipsync_r_onsets": round(move_r, 3),
    "mouth_motion_speech": round(motion_speech, 3) if motion_speech is not None else None,
    "mouth_motion_silence": round(motion_silence, 3) if motion_silence is not None else None,
    "mouth_still_ratio": round(motion_silence / motion_speech, 3) if motion_speech and motion_silence is not None else None,
    "face_motion": round(face_motion, 3),
    "background_motion": round(bg_motion, 3),
    "face_vs_background": round(face_motion / (bg_motion + 1e-9), 2),
    "identity_r": drift,
}))
