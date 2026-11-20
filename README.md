# ElevenLabs Lab

Stephan Munroe’s open notebook for experiments with ElevenLabs. Ideas range from questions about perception and voice to interactive fiction and imaginary radio. The project index holds proposed tests. Published entries pair a result with notes on what worked, what broke and how to reproduce it.

[Visit the lab](https://stephjm24.github.io/elevenlabs-lab/) · [Browse the ideas](IDEAS.md) · [Add an experiment](#add-an-experiment)

## Find your way around

| If you want to… | Start here |
| --- | --- |
| Hear or try a published build | [Experiment gallery](https://stephjm24.github.io/elevenlabs-lab/#experiments) |
| Explore a question for a future build | [Idea notebook](IDEAS.md) |
| See prompts, settings and observations | The build’s README in [projects/](projects/) |

## Add an experiment

1. Copy [the experiment template](projects/_template/) to `projects/<slug>/`. Use a short, lowercase folder name with hyphens.
2. Fill in the README. Lead with the question and result. Give visitors a listening or viewing cue, include the transcript for speech, then record observations and the recipe. Keep prompts in `prompts/` and code in `src/` when relevant.
3. For an inline audio player, put a compact, pre-rendered clip under `docs/media/<slug>/` and link to that same clip from the report. Keep working assets in the project folder. For an external video or interactive demo, use its public URL.
4. Add the entry to the top of [docs/projects.json](docs/projects.json). This file sets the gallery order. Keep unpublished ideas in [IDEAS.md](IDEAS.md).

Use this example as a field guide. Replace the example slug and copy, and omit optional fields that do not apply.

```json
{
  "title": "Your experiment title",
  "pushes": "Voice design",
  "hook": "The question you tested, in one sentence.",
  "audio": "media/your-experiment/sample.mp3",
  "caption": "What to listen for in this sample.",
  "notes": "https://github.com/Stephjm24/elevenlabs-lab/blob/main/projects/your-experiment/README.md"
}
```

Use `link` for a separate playable demo, video or agent. Use `notes` for the written report. Media paths are relative to `docs/`.

## Preview the page

From the repository root, run `python -m http.server 8000 --directory docs` and open <http://localhost:8000>. The static gallery uses plain HTML, CSS and JavaScript. Check narrow and wide layouts, play any new media, and follow the report and transcript links before publishing.

## House rules

- Keep API keys in the ignored `.env` file. Public demos use pre-rendered assets or a public agent widget that needs no key.
- Prefer pre-rendered media. Give live agents a usage cap because conversations spend credits.
- Record models, voices, prompts and settings so someone else can reproduce the result.
- Use designed or library voices, or obtain consent before cloning a real person’s voice.
- Document failures. A clip that shows where the effect breaks can be as informative as the best take.
