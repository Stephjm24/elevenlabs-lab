"""Measure voice-design previews: pitch, loudness, pace, pauses, brightness.

Runs inside the ElevenLabs sandbox (offline, has librosa + pyloudnorm).
Usage: python3 measure.py /workspace/in/*.mp3  -> prints one JSON object per line.
"""
import json
import sys

import librosa
import numpy as np
import pyloudnorm as pyln

SR = 22050

for path in sys.argv[1:]:
    y, sr = librosa.load(path, sr=SR, mono=True)
    dur = len(y) / sr

    # Pitch: probabilistic YIN, voiced frames only.
    f0, voiced, _ = librosa.pyin(y, fmin=50, fmax=800, sr=sr, frame_length=2048, hop_length=512)
    f0v = f0[voiced & ~np.isnan(f0)]
    if len(f0v):
        pitch_med = float(np.median(f0v))
        # Spread in semitones (10th to 90th percentile): how melodic or monotone.
        p10, p90 = np.percentile(f0v, [10, 90])
        pitch_range_st = float(12 * np.log2(p90 / p10))
    else:
        pitch_med, pitch_range_st = None, None

    # Integrated loudness (LUFS).
    meter = pyln.Meter(sr)
    lufs = float(meter.integrated_loudness(y))

    # Pauses: the share of the clip that is silent (30 dB below peak).
    intervals = librosa.effects.split(y, top_db=30)
    speech_secs = float(sum((e - s) for s, e in intervals) / sr)
    pause_ratio = 1 - speech_secs / dur if dur else None

    # Brightness: median spectral centroid.
    centroid = float(np.median(librosa.feature.spectral_centroid(y=y, sr=sr)))

    print(json.dumps({
        "file": path.rsplit("/", 1)[-1],
        "duration_s": round(dur, 2),
        "pitch_median_hz": round(pitch_med, 1) if pitch_med else None,
        "pitch_range_semitones": round(pitch_range_st, 1) if pitch_range_st else None,
        "loudness_lufs": round(lufs, 1),
        "pause_ratio": round(pause_ratio, 3),
        "speech_s": round(speech_secs, 2),
        "brightness_hz": round(centroid),
    }))
