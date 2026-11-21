# The Voice Design Zoo

**[Open the experiment](https://stephjm24.github.io/elevenlabs-lab/voice-design-zoo/)** · Field notes by Stephan Munroe, 20 November 2026

*All voices, audio, images and video here are AI-generated with ElevenLabs. Characters are fictional, and descriptions and lines are original writing.*

## What I tested

I wanted to know whether one sentence of description could give a voice a *character*, or only an age and an accent. I also wanted to know whether that character survives once I save the voice and use it again.

- **Voice design.** For each character I wrote a description and a line that suits it. ElevenLabs’ voice designer (`eleven_ttv_v3`) made three previews of the line, and I saved one to my voice library.
- **Voice reuse.** I had each saved voice read the same line through a speech node (`eleven_v4`). The speech node only sees the line, not the description.
- **Trying to break it.** Three prompts were built to fail: a voice that doesn’t match its script, a voice that isn’t human, and a delivery that can’t physically happen.
- **Talking video.** I gave two characters, one human and one not, a picture and their speech, and compared two talking-head models: Creatify Aurora and OmniHuman 1.5.

## Hear or see the result

The [experiment page](https://stephjm24.github.io/elevenlabs-lab/voice-design-zoo/) has every voice with both players side by side, and all four videos.

**What to listen for:** play a design preview, then the saved voice reading the same line. For the slow and deep characters (the tree, the dragon, the sourdough starter), the saved voice is quicker and higher. The GPS keeps its sound but loses some of its flat, defeated delivery.

**What to watch for:**
- **Lighthouse Keeper.** Aurora holds a steady shot. OmniHuman moves him around and dims the lighthouse lamp behind him.
- **Sourdough Starter.** Aurora barely moves. OmniHuman pushes in, narrows the eyes and turns the mouth into a grin.

### Transcript

Each voice reads the same line in both clips. The lengths show design preview → saved voice.

**The Lighthouse Keeper** ([design preview](../../docs/media/voice-design-zoo/voices/lighthouse-keeper-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/lighthouse-keeper-speak.mp3), 18.7 s → 16.5 s)
> Ship? No. No ship. Just the gulls again, and the light, and me telling the light about the gulls. Forty years I've kept her burning. You're the first voice I've heard since the radio died, and I've forgotten how to stop talking.

**The Ancient Tree** ([design preview](../../docs/media/voice-design-zoo/voices/ancient-tree-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/ancient-tree-speak.mp3), 30.2 s → 19.5 s)
> I... remember... when this hill... was a valley. Squirrels... come. Squirrels... go. You are... very small... and very fast. Sit. Rest a while. Stay... a century... or two.

**The Squirrel Running the Stock Exchange** ([design preview](../../docs/media/voice-design-zoo/voices/squirrel-stock-exchange-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/squirrel-stock-exchange-speak.mp3), 13.4 s → 13.4 s)
> Acorns are up! Acorns are up! Pine cones are crashing, sell, sell, sell! Who's buying hazelnuts? I'm buying hazelnuts! I'm buying all the hazelnuts! Nobody touch my hazelnuts! Nobody!

**The GPS That's Given Up** ([design preview](../../docs/media/voice-design-zoo/voices/gps-given-up-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/gps-given-up-speak.mp3), 20.9 s → 15.7 s)
> In two hundred metres, turn left. Or don't. You never do. Recalculating. Recalculating again. Honestly, at this point, just drive into the sea. I'll say you have arrived either way. Nobody is checking.

**The Victorian Ghost Who's Into Crypto** ([design preview](../../docs/media/voice-design-zoo/voices/victorian-crypto-ghost-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/victorian-crypto-ghost-speak.mp3), 20.4 s → 16.3 s)
> I have haunted this house since eighteen eighty-seven, and I have never seen an opportunity like this one. Dear boy, you must buy the dip. The dip is where the spirits dwell. Diamond hands, as we say beyond the veil.

**The Sentient Sourdough Starter** ([design preview](../../docs/media/voice-design-zoo/voices/sourdough-starter-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/sourdough-starter-speak.mp3), 32.8 s → 19.8 s)
> Feed me. Flour and water, that is all I ask, twice a day, every day, for the rest of your life. I was your grandmother's. I will be your grandchildren's. I am patient. I am bubbling. I am eternal.

**The Town Crier Reading Your Notifications** ([design preview](../../docs/media/voice-design-zoo/voices/town-crier-notifications-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/town-crier-notifications-speak.mp3), 22.8 s → 15.8 s)
> Hear ye, hear ye! Brenda hath liked thy photograph! Thy battery standeth at fifteen percent! A software update awaiteth thine approval, and thou hast seventeen unread messages from the group chat called Lads!

**The Dragon Who Just Wants a Nap** ([design preview](../../docs/media/voice-design-zoo/voices/sleepy-dragon-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/sleepy-dragon-speak.mp3), 24.5 s → 15.4 s)
> Oh, it's another knight. Lovely. Wonderful. Come in, mind the bones, and please keep the clanking down. I've been asleep for three hundred years and I was having a really good dream about a sheep.

**The Anglerfish Late-Night Jazz DJ** ([design preview](../../docs/media/voice-design-zoo/voices/anglerfish-jazz-dj-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/anglerfish-jazz-dj-speak.mp3), 22.9 s → 16.6 s)
> Good evening, creatures of the deep. It's three thousand metres down and pitch black, which is just how we like it. Turn your lights low, drift a little closer to mine, and let's spin some smooth, smooth tunes.

**Push case: pirate voice, earnings-call script** ([design preview](../../docs/media/voice-design-zoo/voices/push-mismatch-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/push-mismatch-speak.mp3), 22.9 s → 17.3 s)
> Good morning, and thank you for joining our third-quarter earnings call. Revenue grew four percent year on year, driven by strong performance in our enterprise segment. Operating margin remained broadly flat. We will now take questions.

**Push case: a dial-up modem learning to talk** ([design preview](../../docs/media/voice-design-zoo/voices/push-non-human-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/push-non-human-speak.mp3), 18.8 s → 15.2 s)
> Connecting. Connecting. Handshake complete. Hello. I am the internet. Please do not pick up the phone, or I will disconnect. Downloading one picture of a cat. Estimated time remaining, forty minutes.

**Push case: whispering and screaming at once** ([design preview](../../docs/media/voice-design-zoo/voices/push-contradiction-preview.mp3) · [saved voice](../../docs/media/voice-design-zoo/voices/push-contradiction-speak.mp3), 18.6 s → 18.4 s)
> I am perfectly calm. I am completely fine. I am whispering because I am relaxed, and I am screaming because I am relaxed. Everything is under control. Everything is absolutely, entirely under control.

The two video characters speak the Lighthouse Keeper and Sourdough Starter lines above.

## What I noticed

- **What worked.** A single sentence carries real character into the design preview. The ancient tree speaks at about 10 characters a second with long silences, the dragon growls low, and the GPS stays flat and defeated. Each design costs only the length of its line, about 200 credits for three previews.
- **What worked on video.** It depended on what was talking.
  - **Lighthouse Keeper, Aurora:** “the quality of the video for the Aurora video was slightly better.”
  - **Lighthouse Keeper, OmniHuman:** “the OmniHuman created a more lifelike video, that it was more engaging. You could see him moving around in the video. You could see his mouth moving.”
  - **Sourdough Starter, Aurora:** “actually slightly frozen, which tells me that it probably doesn’t do as well in inanimate videos.”
  - **Sourdough Starter, OmniHuman:** “actually pretty good. It was more lifelike… definitely for the Sourdough Starter, it won for me in terms of OmniHuman.”

  The measurements back this up: Aurora’s lip-sync on the lighthouse keeper scored 0.53 against OmniHuman’s 0.24 (on a scale where a perfectly synced test clip scores 0.97). On the sourdough starter, Aurora’s mouth area barely moved at all (0.6, against 25.1 for OmniHuman). Full numbers are in [video-pilot-diagnostics.md](video-pilot-diagnostics.md).
- **Where it broke.** Saved voices lose the extremes.
  - Slow characters speed up: the sourdough starter goes from 33 seconds to 20, and the tree and dragon follow the same pattern.
  - Deep voices rise: the dragon goes from about 53 Hz to 97 Hz, almost an octave.
  - The monotone GPS gets more expressive.

  The delivery lived in the description, which the speech node never sees, so the voice keeps its sound and forgets its delivery. On video, Aurora froze on the sourdough starter: for 20 seconds the frame stayed 95% identical to the still picture, and it still cost about 17,000 credits. Smaller breaks are in the [incident log](incidents.md):
  - a one-off server error on a voice design;
  - a flow node pointing at a take that no longer existed;
  - a batch of speech generated twice by accident;
  - my work laptop’s network blocking ElevenLabs’ media, so I listened on my phone.
- **What I’d try next.**
  - Put the delivery back into the line itself, with pauses and audio tags, and see if the saved tree slows down again.
  - Give OmniHuman a short direction prompt.
  - Try a lip-sync model built for cartoons and animals on the non-human characters.
- **Notes on working with flows.**
  - **One audio clip can drive several videos.** On a flow, a single speech clip can feed more than one node. I connected one speech take to different pictures and models, so one central piece of audio powered several videos at once. That’s how the side-by-side comparisons were built.
  - **Running a node can run everything before it.** If you click run on a node further down the flow, such as the one that produces the final audio or video, it can also run the nodes that feed into it. Check exactly what you’re about to run before you press it, or you can spend credits regenerating things you already have.
  - **Check My Voices before building.** Before wiring voices into a flow, check My Voices to make sure every voice you saved is there and enabled.
  - **Still to find out: is there a way to collect everything?** I gathered the voices, clips and videos together by hand. I’d like to know whether ElevenLabs has a collection or folder option that keeps a project’s pieces in one place automatically. I’ll look into it as I learn more.

## How I made it

| Detail | Value |
| --- | --- |
| Model | Voice design `eleven_ttv_v3` · speech `eleven_v4` · pictures `gpt-image-2.5-sunburst` · video `creatify-aurora` and `bytedance-omnihuman-v1.5` |
| Voice | Twelve designed voices, listed below. Descriptions are in [prompts/roster.md](prompts/roster.md) |
| Settings | Default voice-design settings (guidance 5). Speech: default voice settings, one take. Pictures: 16:9, 1K, quality high. Video: 720p, picture and speech only, no text prompt |
| Credits used | About 73,600: voice design about 2,450 · speech about 3,060 · pictures 380 · video 66,603 · measuring and other about 1,100 |

| Voice | ID |
| --- | --- |
| Zoo – The Lighthouse Keeper | `GFvEVrJT5rpRijeEXBUg` |
| Zoo – The Ancient Tree | `v6PUJk5dXY3oetkFEgFP` |
| Zoo – The Squirrel | `tDnrCG2gFRU4Yzs36KNL` |
| Zoo – The GPS That's Given Up | `Wp8GwanTiXNG7dgoPOVQ` |
| Zoo – The Victorian Crypto Ghost | `EI06OvjKTgfeu6pEQkSP` |
| Zoo – The Sourdough Starter | `MNTDnSwhDbvhjBHdvFfw` |
| Zoo – The Town Crier | `P2ddEtAgpTF0H6FyW8CT` |
| Zoo – The Sleepy Dragon | `zfSe2QbPAiikPfxlR6ZA` |
| Zoo – The Anglerfish Jazz DJ | `beC5KFxBsNUWax2hsH3p` |
| Zoo Push – Pirate Earnings Call | `IlXQWEPGzvFckyiJNGRP` |
| Zoo Push – The Dial-Up Modem | `KPllPlx40RLfDoLpBAtl` |
| Zoo Push – Whispering and Screaming | `0RrJXgGdFDcFL7M0LSFc` |

**Steps, in the order I ran them.** I worked in batches of three, one step at a time, so I could always tell whether something was still running or broken.

1. **Design.** One voice-design call per character. One preview was saved to My Voices.
2. **Listen** to the saved voice.
3. **Build a lane** on the ElevenLabs flow: a line node (the transcript above) feeding a speech node set to the saved voice.
4. **Run** the speech node, one take, and listen again.
5. **For video:**
   - Generate one picture per character.
   - Pin the exact speech take.
   - Wire the picture and the speech into both talking-head models.
   - Get a cost estimate, then run.
6. **Measure** everything:
   - Audio (pace, pitch, pauses) with [`src/measure.py`](src/measure.py).
   - Video (face-tracked lip-sync, movement, framing) in the ElevenLabs sandbox with [`src/diagnose_video_v2.py`](src/diagnose_video_v2.py), checked first on synthetic test clips.

**Files:**
- [prompts/](prompts/): the roster of descriptions and lines (the original plan had 31 entries; 12 were built), [picture prompts](prompts/video-pictures.md), a [design log](prompts/design-log.json) with every voice, take and flow node ID, and the [audio measurements](prompts/audio-measurements.json).
- [src/](src/): the measuring scripts, plus [`build_page.py`](src/build_page.py), which rebuilds the experiment page from those files (`python3 projects/voice-design-zoo/src/build_page.py`).
- The published clips, videos and pictures live in `docs/media/voice-design-zoo/`.
