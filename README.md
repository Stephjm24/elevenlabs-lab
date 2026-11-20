# ElevenLabs Lab 🎙️

A public playground for pushing ElevenLabs as far as it will go: voices, voice design, voice agents, speech-to-text, sound, image, video and lipsync. Nothing here has to be useful. Each project is an experiment, published so anyone can hear the result.

## Projects

| # | Project | What it pushes | Status | Demo |
|---|---------|----------------|--------|------|
| – | _nothing yet, see [IDEAS.md](IDEAS.md)_ | | | |

## Layout

```
projects/<slug>/     one folder per experiment (copy projects/_template)
  README.md          what it is, how it was made, what broke
  prompts/           voice-design prompts, scripts, agent prompts
  assets/            final audio/video/images (keep them small, use mp3)
  src/               any code
site/                static gallery, published with GitHub Pages
```

## House rules

1. **Never commit an API key.** Keys go in `.env` (git-ignored). Public pages use pre-rendered audio, or a public agent widget that needs no key.
2. **Pre-render where possible.** A static page full of mp3s costs nothing when it goes viral. A live agent widget spends credits on every conversation, so give it a usage cap.
3. **Write down the recipe.** Every project README records the model, the voice IDs, the prompts and the settings, so a result can be made again.
4. **No cloning real people without their consent.** Designed voices and library voices are fine.
5. **Log the failures.** "Here's where it fell apart" is half the fun of pushing limits.
