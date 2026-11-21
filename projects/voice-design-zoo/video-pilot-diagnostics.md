# Talking-head video: OmniHuman 1.5 vs Creatify Aurora, human vs non-human

Two characters from the zoo, each given a picture (`gpt-image-2.5-sunburst`, 1280×720, warm 3D animated-film style) and its zoo speech take, then animated by both models at 720p with no text prompt. Identical inputs per character, so differences come from the model.

| | Lighthouse Keeper (human) | Sourdough Starter (non-human, face made of bubbles inside a glass jar) |
|---|---|---|
| Picture | gen `TnafsZcvT55kg1RIohTD` | gen `iMc6A2qR0nIomaky5clK` |
| Speech | 16.48 s (`65QmmuO4IuKKHDDvPa1s`, pinned) | 19.84 s (`Og10AJRa0kgyTLZTWygh`) |

## Method
Measured in the ElevenLabs sandbox with `src/diagnose_video_v2.py`:
- **Face tracking**: the face from the source picture is template-matched in every frame (position and zoom), so the mouth box follows the face even when the model moves the camera.
- **Lip-sync score**: how closely the mouth area's change from its resting look follows the loudness of the speech (best match within ±320 ms). Validated on synthetic clips: perfectly synced 0.97, random 0.01, including with a moving, zooming camera.
- **Mouth activity**: how much the mouth area changes while speaking (same scale for all four clips).
- Plus framing (similarity to the picture, every second), lighting (mean brightness, every second), background motion, cost, render time, file size.

## Results

| Measure | Lighthouse · Aurora | Lighthouse · OmniHuman | Sourdough · Aurora | Sourdough · OmniHuman |
|---|---|---|---|---|
| Credits | 14,422 | 15,978 | 16,967 | 19,236 |
| ≈ credits per second | 875 | 970 | 855 | 970 |
| Render time | ≤5.5 min | ~6.5 min | ≤6 min | ~6 min |
| Output | 1280×704, 16.7 s, 4.0 MB | 1248×704, 16.7 s, 7.7 MB | 1280×704, 20.0 s, 2.6 MB | 1248×704, 20.2 s, 7.5 MB |
| **Lip-sync score** (0.97 perfect / 0.01 random) | **0.53** | 0.24 | 0.21 (at a 320 ms lag: noise) | 0.17 |
| **Mouth activity while speaking** | 11.8 | 17.6 | **0.6** (barely moves) | **25.1** |
| Face movement (range across the frame) | 3% × 2% | 22% × 23%, zoom 0.8–1.1 | 0% (frozen) | 13% × 28%, zoom 0.8–1.4 |
| Similarity to the picture | 0.90–0.96 | 0.32–0.99 | 0.95 every second | 0.58–0.99 |
| Brightness range | 69–72 | 51–82 | 93–94 | 92–104 |
| Background motion | 0.52 | 1.69 | 0.12 | 1.25 |
| Tracking confidence (median) | 0.88 | 0.71 | 0.98 | 0.73 |

## What it means
- **Human: Aurora wins.** Its mouth follows the speech twice as closely as OmniHuman's (0.53 vs 0.24), the shot stays locked off, the lighting is steady, and it's 10% cheaper and lighter. OmniHuman is livelier (it moves the camera, the head and the lighting) but its lip-sync is looser.
- **Non-human: the result flips.** Aurora **essentially didn't animate the sourdough starter**: the mouth area changed about 20× less than on the human, and the frame stayed 95% identical to the still picture for 20 seconds. That's a near-still image for ~17,000 credits. OmniHuman **did bring it to life** (the most mouth activity of all four clips, and the dough and jar moving and reframing), but the movement only loosely follows the words (0.17).
- **Rule of thumb:** Aurora for people (accurate, predictable); OmniHuman for anything that isn't a person (it will at least animate it); neither gives tight lip-sync on a non-human face.
- **Caveats:** OmniHuman's moving shots give lower tracking confidence (0.71–0.73), so its lip-sync scores carry more uncertainty than Aurora's. Numbers measure *movement and timing*, not whether it looks good; that's the human verdict below.

## Human verdict (Steph's field notes, 20 Nov 2026)
Watched all four clips on a phone. Layman's notes, not technical:

- **Lighthouse Keeper · OmniHuman:** "a more lifelike video, more engaging. You could see him moving around in the video. You could see his mouth moving."
- **Lighthouse Keeper · Aurora:** "the quality of the video was slightly better."
- **Lighthouse verdict:** *mixed*. Aurora gives the better picture quality, OmniHuman the more lifelike, engaging performance.
- **Sourdough Starter · Aurora:** "actually slightly frozen, which tells me that it probably doesn't do as well in inanimate videos."
- **Sourdough Starter · OmniHuman:** "actually pretty good. It was more lifelike." **OmniHuman wins the sourdough starter.**

## Numbers vs eyes
- **They agree on the sourdough starter.** The frozen Aurora clip that the numbers flagged (mouth activity 0.6, frame 95% identical to the still) is what Steph saw. OmniHuman animated it and won.
- **They disagree on the lighthouse keeper, usefully.** The numbers favour Aurora (tighter lip-sync, steadier shot, cleaner image). Steph found OmniHuman more engaging *because* of the movement the numbers count against it. The measurements reward accuracy and stability, but a viewer also rewards performance. Both are true: Aurora is the cleaner talking head, OmniHuman the better actor.
- **Overall pick:** OmniHuman if you want a character to feel alive (and the only option that worked for a non-human). Aurora if you need a clean, accurate, predictable talking head of a person.
