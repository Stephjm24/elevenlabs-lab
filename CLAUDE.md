# ElevenLabs Lab: working instructions

This is a public playground for finding out what ElevenLabs can really do. Every experiment is published (GitHub repo `Stephjm24/elevenlabs-lab`, gallery on GitHub Pages). Experiments don't need a purpose. They should be fun, ambitious and honest about where things break.

**One project per chat.** Each chat goes deep on a single experiment from `IDEAS.md` (or a new one), from first test to published result.

---

## 1. Start of every chat

1. **Load context.** Read `claude/lab-plan.md` (backlog and what's built) and `claude/elevenlabs-findings.md` (everything learned so far) from the ElevenLabs Projects project.
2. **Get the repo.** Attach `Stephjm24/elevenlabs-lab` with push access and clone it. The cloud workspace starts empty each chat, so GitHub is the source of truth. If the repo doesn't exist yet, scaffold from the lab plan and remind the user to create it.
3. **Check the budget.** Call `account_get_usage` and note the characters left this cycle.
4. **Confirm the project.** If the user hasn't named one, suggest the next best one from the backlog. Then state in a few lines the question this experiment is trying to answer and which ElevenLabs capabilities it will stress.

## 2. How to run an experiment

Work in four phases and tell the user when you move between them.

**Explore.** Before building, read the relevant ElevenLabs guides (`creative_get_guide`) and model guides (`creative_get_model_guide`) and summarise for the user what the capability can do, its main settings and its known limits. Then run small, cheap probes, varying one thing at a time.

**Push.** Deliberately try to break it: edge cases, extreme prompts, long inputs, odd languages, emotional extremes, chaining one output into another. Note exactly where quality drops off. The failures are content.

**Build.** Make the finished piece in `projects/<slug>/`, copied from `projects/_template/`:
- `README.md` records the recipe (models, voice IDs, design prompts, settings, credits used), the results and "where it broke"
- `prompts/` holds every script, voice-design prompt and agent prompt used
- `assets/` holds final outputs (mp3 over wav, compressed video, small images)
- `src/` holds any code

**Publish.**
- Add an entry to `docs/projects.json` (`title`, `hook`, `pushes`, `audio` and/or `link`) and a row to the README project table.
- Commit with a clear message and push to `main`. Ask before the first push of each chat.
- Update `claude/lab-plan.md` ("Built so far") and append findings to `claude/elevenlabs-findings.md`.

## 3. ElevenLabs tool rules

- **Credits are real money.** Never repeat a generation call to retry, because each call charges again. Keep `generations_count` at its default. Ask before anything long or expensive (long videos, full audiobooks, batch runs). Report the credits each project used.
- **Voice IDs** come only from `creative_list_voices`, `creative_design_voice`/`creative_save_designed_voice`, or the user. Never from memory.
- **Chained work** (voiceover → lipsync, image → video): call `creative_create_flow` first and pass its `flow_id` to every step.
- **Don't poll** generations. The tools return when a job starts and the flow view shows progress. Use `creative_get_flow_run_status` once when you need the generation IDs.
- **Voice agents:** build with `agents_generate` or `agents_create`, change one area at a time with `agents_update_*`, and add tests (`agents_create_test` + `agents_run_tests`) before an agent is embedded publicly. A public widget spends credits on every conversation, so set usage limits.
- **Getting files into the repo:** download generated assets into `projects/<slug>/assets/`. If an asset can only be reached through the flow URL, say so and ask the user to export it.
- If a capability is missing from the tools, call `get_more_tools` describing it, then look for a workaround (the API via the CLI, ffmpeg locally).

## 4. Public-safety rules

- **No secrets in git.** API keys only in `.env` (ignored). Public pages use pre-rendered media or a public agent widget.
- **No cloning or imitating real people**: no celebrity voices, no "in the style of [real person]" impressions, no real people's likenesses in images or video. Designed voices, library voices and fictional characters only.
- **Text you didn't write:** public domain only (published before 1929) or original writing.
- **Label it as AI.** Every published page and README says the voices and media are AI-generated with ElevenLabs.

## 5. How to talk to the user

- The goal is learning what ElevenLabs can do, so explain as you go: what a setting changed, why something failed, how it compares to the last probe. Keep it short. One or two sentences per finding.
- Share clips and drafts as soon as they're worth hearing rather than saving everything for the end.
- End each chat with three things: what was built (with the link), the two or three most surprising findings, and a suggestion for the next experiment.
