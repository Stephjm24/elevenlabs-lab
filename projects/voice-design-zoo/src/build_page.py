"""Build docs/voice-design-zoo/index.html in the lab's notebook design.

The page links the site's shared docs/styles.css (masthead, Manrope, colours, notes,
index rows, footer) plus docs/voice-design-zoo/zoo.css for the few extra pieces
(players, chart, video grid, table). Reads prompts/roster.json and
prompts/audio-measurements.json.

Run from the repo root:  python3 projects/voice-design-zoo/src/build_page.py
"""
import json
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJ = ROOT / "projects" / "voice-design-zoo"
OUT = ROOT / "docs" / "voice-design-zoo"
MEDIA = "../media/voice-design-zoo"
REPO = "https://github.com/Stephjm24/elevenlabs-lab"

roster = {r["id"]: r for r in json.loads((PROJ / "prompts/roster.json").read_text())}
meas = json.loads((PROJ / "prompts/audio-measurements.json").read_text())

ZOO = ["lighthouse-keeper", "ancient-tree", "squirrel-stock-exchange", "gps-given-up",
       "victorian-crypto-ghost", "sourdough-starter", "town-crier-notifications",
       "sleepy-dragon", "anglerfish-jazz-dj"]
PUSH = ["push-mismatch", "push-non-human", "push-contradiction"]
PUSH_NAMES = {"push-mismatch": "Pirate voice, earnings-call script",
              "push-non-human": "A dial-up modem learning to talk",
              "push-contradiction": "Whispering and screaming at once"}
UNRELIABLE_PITCH = {"push-mismatch", "push-non-human"}


def name_of(vid):
    return PUSH_NAMES.get(vid, roster[vid]["name"])


def row(vid, kind):
    r, m = roster[vid], meas[vid]
    p, s = m["preview"], m["speak"]
    change = (s["duration_s"] - p["duration_s"]) / p["duration_s"] * 100
    state = "same" if abs(change) < 2 else f"{change:+.0f}%".replace("-", "−")
    asked = (f'<h3>What I wanted to know</h3><p>{e(r["question"])}</p>' if r.get("question") else "")
    pitch = f'{p["pitch_median_hz"]:.0f} → {s["pitch_median_hz"]:.0f} Hz'
    if vid in UNRELIABLE_PITCH:
        pitch += " (unreliable: the voice is too raspy or noisy to track)"
    return f"""
      <details class="entry" id="{vid}">
        <summary><span class="entry-title">{e(name_of(vid))}</span><span class="kind">{kind}</span><span class="state">{state}</span></summary>
        <div class="entry-note">
          {asked}
          <h3>Description I gave it</h3>
          <p>{e(r["description"])}</p>
          <h3>Transcript</h3>
          <p>“{e(r["text"])}”</p>
          <div class="players">
            <figure><figcaption>Design preview <span>follows the description</span></figcaption>
              <audio controls preload="none" src="{MEDIA}/voices/{vid}-preview.mp3" aria-label="Design preview: {e(name_of(vid))}"></audio></figure>
            <figure><figcaption>Saved voice <span>reads the same line</span></figcaption>
              <audio controls preload="none" src="{MEDIA}/voices/{vid}-speak.mp3" aria-label="Saved voice: {e(name_of(vid))}"></audio></figure>
          </div>
          <p class="measure">Length {p["duration_s"]:.1f} → {s["duration_s"]:.1f} s · pace {p["chars_per_speech_s"]:.0f} → {s["chars_per_speech_s"]:.0f} characters a second · pitch {pitch}</p>
        </div>
      </details>"""


def pace_chart():
    ids = sorted(ZOO + PUSH, key=lambda v: meas[v]["preview"]["chars_per_speech_s"])
    W, step, left, right, top = 760, 28, 250, 24, 34
    lo, hi = 6, 20
    H = top + step * len(ids) + 34
    x = lambda v: left + (v - lo) / (hi - lo) * (W - left - right)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="chart-title">'
           '<title id="chart-title">Speaking pace of each voice: design preview compared with the saved voice reading the same line</title>']
    for t in range(lo, hi + 1, 2):
        out.append(f'<line x1="{x(t):.1f}" x2="{x(t):.1f}" y1="{top-12}" y2="{H-28}" class="grid"/>'
                   f'<text x="{x(t):.1f}" y="{H-10}" class="tick" text-anchor="middle">{t}</text>')
    out.append(f'<text x="{W-right}" y="{top-18}" class="tick" text-anchor="end">characters a second</text>')
    for i, v in enumerate(ids):
        y = top + i * step + step / 2
        a, b = meas[v]["preview"]["chars_per_speech_s"], meas[v]["speak"]["chars_per_speech_s"]
        label = name_of(v).replace("The ", "")
        label = label if len(label) < 33 else label[:31] + "…"
        out.append(f'<text x="{left-12}" y="{y+4:.1f}" class="lab" text-anchor="end">{e(label)}</text>'
                   f'<line x1="{x(a):.1f}" x2="{x(b):.1f}" y1="{y:.1f}" y2="{y:.1f}" class="link"/>'
                   f'<circle cx="{x(a):.1f}" cy="{y:.1f}" r="5.5" class="pre"><title>Design preview: {a}</title></circle>'
                   f'<circle cx="{x(b):.1f}" cy="{y:.1f}" r="5.5" class="spk"><title>Saved voice: {b}</title></circle>')
    out.append("</svg>")
    return "\n".join(out)


def clip(char, title, notes):
    return f"""
      <article class="clip" id="{char}-video">
        <h3>{e(title)}</h3>
        <div class="clip-grid">
          <div class="vids">
            <figure><figcaption>Creatify Aurora</figcaption>
              <video controls preload="none" playsinline poster="{MEDIA}/video/{char}-aurora-poster.jpg" src="{MEDIA}/video/{char}-aurora.mp4" aria-label="{e(title)}, Creatify Aurora"></video></figure>
            <figure><figcaption>OmniHuman 1.5</figcaption>
              <video controls preload="none" playsinline poster="{MEDIA}/video/{char}-omnihuman-poster.jpg" src="{MEDIA}/video/{char}-omnihuman.mp4" aria-label="{e(title)}, OmniHuman 1.5"></video></figure>
          </div>
          <aside class="note field-note" aria-label="My notes on {e(title)}">
            <div class="note-header"><span class="pin" aria-hidden="true"></span><h4>My notes</h4></div>
            <div class="note-body">{notes}</div>
          </aside>
        </div>
        <figure class="frames"><img src="{MEDIA}/video/{char}-frames.jpg" alt="Frames from the start, middle and end of each clip. Aurora on the top row, OmniHuman below." loading="lazy" width="976" height="424">
          <figcaption>Start, middle and end of each clip. Aurora on top, OmniHuman below.</figcaption></figure>
      </article>"""


LIGHTHOUSE_NOTES = """
              <p><b>Aurora.</b> “The quality of the video for the Aurora video was slightly better.”</p>
              <p><b>OmniHuman.</b> “It seemed to me that the OmniHuman created a more lifelike video, that it was more engaging. You could see him moving around in the video. You could see his mouth moving.”</p>
              <p><b>Verdict.</b> “More variable, because the Aurora video was better quality, while the OmniHuman one was more lifelike and engaging.”</p>"""
SOURDOUGH_NOTES = """
              <p><b>Aurora.</b> “It was actually slightly frozen, which tells me that it probably doesn’t do as well in inanimate videos.”</p>
              <p><b>OmniHuman.</b> “It was actually pretty good. It was more lifelike.”</p>
              <p><b>Verdict.</b> “Definitely for the Sourdough Starter, it won for me in terms of OmniHuman.”</p>"""

TABLE = [
    ("Lip-sync score", "0.53", "0.24", "0.21*", "0.17"),
    ("Mouth movement while speaking", "11.8", "17.6", "0.6", "25.1"),
    ("Movement in the shot", "Almost none", "Head moves, lamp dims", "None (frozen)", "Pushes in, eyes narrow"),
    ("Match to the still picture", "90–96%", "32–99%", "95% throughout", "58–99%"),
    ("Credits", "14,422", "15,978", "16,967", "19,236"),
    ("Render time", "Up to 5.5 min", "About 6.5 min", "Up to 6 min", "About 6 min"),
]
table_rows = "\n".join(
    f'<tr><th scope="row">{e(r[0])}</th>' + "".join(f"<td>{e(c)}</td>" for c in r[1:]) + "</tr>" for r in TABLE)

html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Twelve voices designed from a sentence each, three attempts to break it, and two of them made to talk on video. Field notes by Stephan Munroe.">
  <title>The Voice Design Zoo · ElevenLabs Lab</title>
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="zoo.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="mast wrap">
    <a class="brand" href="../"><span aria-hidden="true" class="spine"></span>ElevenLabs Lab</a>
    <nav aria-label="Main navigation"><a href="../#notebook">Project index</a><a href="{REPO}">GitHub</a></nav>
  </header>
  <main id="main" class="wrap">
    <section class="feature" aria-labelledby="feature-title">
      <div class="lead">
        <p class="byline">Field notes by Stephan Munroe · 20 November 2026</p>
        <h1 id="feature-title">The Voice Design Zoo</h1>
        <p class="intro">I gave ElevenLabs one sentence about a character, such as a lighthouse keeper alone for forty years, a GPS that has given up or a sourdough starter that will outlive us all, and asked it to design a voice. Then I saved each voice and had it read the same line again, to see whether the character survived.</p>
        <a class="index-link" href="#voices">Listen to the zoo</a>
      </div>
      <aside class="note" aria-labelledby="note-title">
        <div class="note-header"><span class="pin" aria-hidden="true"></span><h2 id="note-title">What I wanted to know</h2></div>
        <ul class="questions">
          <li><a href="#voices">Can a description give a voice a character, or only an age and an accent?</a></li>
          <li><a href="#noticed">Does the character survive when I reuse the voice?</a></li>
          <li><a href="#video">Can a sourdough starter talk on video?</a></li>
        </ul>
      </aside>
    </section>

    <section class="zoo-section" aria-labelledby="tested-title">
      <div class="section-head"><h2 id="tested-title">What I tested</h2></div>
      <div class="prose">
        <p><b>Voice design.</b> For each character I wrote a description and a line that suits it. ElevenLabs’ voice designer (<code>eleven_ttv_v3</code>) made three previews of the line, and I saved one to my voice library.</p>
        <p><b>Voice reuse.</b> I then had each saved voice read the same line through a speech node (<code>eleven_v4</code>). The speech node only sees the line, not the description, so this shows what the voice keeps once the instructions are gone.</p>
        <p><b>Trying to break it.</b> Three prompts were built to fail: a voice that doesn’t match its script, a voice that isn’t human, and a delivery that can’t physically happen.</p>
        <p><b>Talking video.</b> I gave two characters, one human and one not, a picture and their speech, and tried two talking-head models on each.</p>
      </div>
    </section>

    <section class="index zoo-section" id="voices" aria-labelledby="voices-title">
      <div class="section-head"><h2 id="voices-title">Hear the result</h2><a href="#chart">Pace chart</a></div>
      <p class="lede-note">Open a row to hear the design preview and the saved voice side by side. The number on each row is how the length of the line changed when the saved voice read it.</p>
      {''.join(row(v, "Character") for v in ZOO)}
      {''.join(row(v, "Push case") for v in PUSH)}
    </section>

    <section class="zoo-section" id="video" aria-labelledby="video-title">
      <div class="section-head"><h2 id="video-title">Two of them on video</h2></div>
      <p class="lede-note">Each character got a picture (GPT Image 2.5, warm 3D animated-film style) and its zoo speech. Then two talking-head models animated it with the same inputs at 720p. I watched all four on my phone and wrote down what I saw.</p>
      {clip("lighthouse", "The Lighthouse Keeper", LIGHTHOUSE_NOTES)}
      {clip("sourdough", "The Sourdough Starter", SOURDOUGH_NOTES)}
      <div class="table-wrap">
        <table>
          <caption>What the measurements said. Lip-sync and mouth movement were measured with face tracking: a perfectly synced test clip scores 0.97 and random movement 0.01.</caption>
          <thead><tr><td></td><th scope="col">Lighthouse · Aurora</th><th scope="col">Lighthouse · OmniHuman</th><th scope="col">Sourdough · Aurora</th><th scope="col">Sourdough · OmniHuman</th></tr></thead>
          <tbody>{table_rows}</tbody>
        </table>
        <p class="small">* At that level the score is noise: the mouth hardly moved.</p>
      </div>
    </section>

    <section class="zoo-section" id="noticed" aria-labelledby="noticed-title">
      <div class="section-head"><h2 id="noticed-title">What I noticed</h2></div>
      <div class="prose">
        <h3>What worked</h3>
        <p>A single sentence really does carry character into the design preview. The ancient tree speaks at about 10 characters a second with long silences, the dragon growls low, and the GPS stays flat and defeated. Each design costs only the length of its line, about 200 credits for three previews.</p>
        <p>On video, the result depended on what was talking. For the lighthouse keeper, Aurora gave the cleaner picture and the tighter lip-sync, and OmniHuman gave the more lifelike performance. For the sourdough starter, only OmniHuman brought it to life.</p>

        <h3>Where it broke</h3>
        <p><b>Saved voices lose the extremes.</b> Reading the same line, the saved voices drift towards the middle:</p>
        <ul>
          <li>Slow characters speed up. The sourdough starter reads its line in 20 seconds instead of 33.</li>
          <li>Deep voices rise. The dragon goes from about 53 Hz to 97 Hz, almost an octave.</li>
          <li>The monotone GPS gets more expressive.</li>
        </ul>
        <p>The slowness and the growl were in the description, and the speech node never sees the description. The voice keeps its sound but forgets its delivery.</p>
      </div>
      <figure class="chart" id="chart">
          {pace_chart()}
          <figcaption><span class="key pre"></span>Design preview <span class="key spk"></span>Saved voice reading the same line. Nearly every line moves right, towards an average pace.</figcaption>
        </figure>
      <div class="prose">
        <p><b>Aurora froze on the sourdough starter.</b> For 20 seconds the frame stayed 95% identical to the still picture. A face made of bubbles behind glass doesn’t seem to count as a face, and it still cost about 17,000 credits.</p>
        <p><b>Smaller breaks.</b></p>
        <ul>
          <li>One voice design failed with a server error and worked on an identical retry.</li>
          <li>A flow node pointed at a take that no longer existed until I pinned the real one.</li>
          <li>One batch of speech was generated twice by accident.</li>
          <li>My work laptop’s network blocked ElevenLabs’ media, so all my listening happened on my phone.</li>
        </ul>
        <p>The full list is in the <a href="{REPO}/blob/main/projects/voice-design-zoo/incidents.md">incident log</a>.</p>

        <h3>What I’d try next</h3>
        <ul>
          <li>Put the delivery back into the line itself, with pauses and audio tags, and see if the saved tree slows down again.</li>
          <li>Give OmniHuman a short direction prompt, and try a lip-sync model built for cartoons and animals on the non-human characters.</li>
          <li>Animate the rest of the zoo with OmniHuman.</li>
        </ul>
      </div>
    </section>

    <section class="zoo-section" id="recipe" aria-labelledby="recipe-title">
      <div class="section-head"><h2 id="recipe-title">How I made it</h2><a href="{REPO}/tree/main/projects/voice-design-zoo">Project folder</a></div>
      <div class="table-wrap">
        <table class="recipe">
          <thead><tr><th scope="col">Detail</th><th scope="col">Value</th></tr></thead>
          <tbody>
            <tr><th scope="row">Voice design</th><td><code>eleven_ttv_v3</code>, default settings. One call per character gives three previews, and I kept one.</td></tr>
            <tr><th scope="row">Speech</th><td><code>eleven_v4</code>, default voice settings, one take. On the flow, each character is a line node feeding a speech node.</td></tr>
            <tr><th scope="row">Pictures</th><td><code>gpt-image-2.5-sunburst</code>, 16:9, one image each</td></tr>
            <tr><th scope="row">Talking video</th><td>Creatify Aurora and OmniHuman 1.5, 720p, picture and speech only</td></tr>
            <tr><th scope="row">Voices</th><td>Twelve designed voices. Names, IDs and every prompt are in the <a href="{REPO}/blob/main/projects/voice-design-zoo/README.md">lab notes</a>.</td></tr>
            <tr><th scope="row">Credits used</th><td>About 73,600: voices and speech about 5,500, pictures 380, video 66,603, measuring and other about 1,100</td></tr>
          </tbody>
        </table>
      </div>
      <div class="prose">
        <p>I worked in batches of three, one step at a time: design, save, listen, build the flow, run, listen again. That way I could always tell whether something was still running or actually broken.</p>
      </div>
    </section>
  </main>
  <footer class="wrap"><strong>Stephan Munroe</strong><span>All voices, audio, images and video here are AI-generated with ElevenLabs. Characters are fictional, and descriptions and lines are original writing.</span></footer>
  <script>
    // Open a voice row when the page is visited with its #id (e.g. from the landing page).
    function openTarget() {{
      const el = location.hash && document.getElementById(location.hash.slice(1));
      if (el && el.tagName === "DETAILS") {{ el.open = true; el.scrollIntoView(); }}
    }}
    window.addEventListener("hashchange", openTarget);
    openTarget();
  </script>
</body>
</html>
"""

CSS = """/* Voice Design Zoo: additions to the shared ../styles.css. Uses its colours and type. */
.zoo-section { border-top: 2px solid var(--ink); padding-bottom: 2.5rem; scroll-margin-top: 1rem; }
.prose { max-width: 65ch; }
.prose p + p, .prose ul + p, .prose p + ul { margin-top: .9rem; }
.prose h3 { font-size: 1.25rem; font-weight: 600; letter-spacing: -.025em; margin: 2rem 0 .5rem; }
.prose h3:first-child { margin-top: 0; }
.prose ul { margin: .5rem 0 0; padding-left: 1.25rem; }
.prose li + li { margin-top: .35rem; }
code { font-size: .9em; background: #efefe7; padding: .05em .3em; border-radius: 3px; }
.lede-note { color: var(--muted); max-width: 65ch; margin: -.5rem 0 1.5rem; }
.entry-note p + h3 { margin-top: 1rem; }
.entry-note > p { margin-bottom: .25rem; }
.players { display: grid; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); gap: 1rem; margin: 1.25rem 0 .75rem; }
.players figure { margin: 0; }
.players figcaption { font-weight: 600; font-size: .875rem; margin-bottom: .35rem; }
.players figcaption span { font-weight: 400; color: var(--muted); margin-left: .35rem; }
.players audio { width: 100%; }
.measure { font-size: .875rem; color: var(--muted); }
.chart { margin: 1.75rem 0; max-width: 52rem; }
.chart svg { width: 100%; height: auto; display: block; }
.chart .grid { stroke: var(--rule); }
.chart .tick, .chart .lab { fill: var(--muted); font: 500 13px Manrope, sans-serif; }
.chart .lab { fill: var(--ink); }
.chart .link { stroke: #9a9c92; stroke-width: 2; }
.chart .pre { fill: var(--page); stroke: var(--ink); stroke-width: 1.75; }
.chart .spk { fill: var(--highlight); stroke: var(--ink); stroke-width: 1.75; }
.chart figcaption { font-size: .875rem; color: var(--muted); margin-top: .5rem; }
.key { display: inline-block; width: .7rem; height: .7rem; border-radius: 50%; border: 1.75px solid var(--ink); vertical-align: -.05rem; margin: 0 .3rem 0 0; }
.key.pre { background: var(--page); }
.key.spk { background: var(--highlight); margin-left: .75rem; }
.clip { padding: 1.5rem 0 2rem; border-top: 1px solid var(--rule); }
.clip:first-of-type { border-top: 0; padding-top: 0; }
.clip h3 { font-size: 1.5rem; font-weight: 600; letter-spacing: -.035em; margin-bottom: 1rem; }
.clip-grid { display: grid; grid-template-columns: 1fr 17rem; gap: 2rem; align-items: start; }
.vids { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.vids figure { margin: 0; }
.vids figcaption { font-weight: 600; font-size: .875rem; margin-bottom: .35rem; }
.vids video { width: 100%; display: block; border: 1px solid var(--ink); background: var(--ink); }
.field-note { transform: rotate(-1deg); }
.field-note h4 { margin: 0; font-size: .875rem; }
.note-body { padding: 1rem 1.5rem 1.25rem; }
.note-body p { font-size: .95rem; line-height: 1.45; }
.note-body p + p { margin-top: .75rem; }
.frames { margin: 1.5rem 0 0; }
.frames img { width: 100%; height: auto; display: block; }
.frames figcaption, .small { font-size: .875rem; color: var(--muted); margin-top: .5rem; }
.table-wrap { overflow-x: auto; margin-top: 1rem; }
table { width: 100%; border-collapse: collapse; font-size: .95rem; }
caption { text-align: left; color: var(--muted); font-size: .875rem; padding-bottom: .75rem; max-width: 65ch; }
th, td { text-align: left; padding: .7rem .75rem .7rem 0; border-bottom: 1px solid var(--rule); vertical-align: top; }
thead th { font-weight: 600; font-size: .875rem; border-bottom: 2px solid var(--ink); }
tbody th { font-weight: 600; color: var(--muted); font-size: .875rem; }
table.recipe { max-width: 48rem; }
table.recipe tbody th { width: 9rem; }
@media (max-width: 60rem) {
  .clip-grid { grid-template-columns: 1fr; }
  .field-note { max-width: 32rem; }
}
@media (max-width: 36rem) {
  .vids { grid-template-columns: 1fr; }
}
"""

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "index.html").write_text(html)
(OUT / "zoo.css").write_text(CSS)
print("wrote", OUT / "index.html", len(html), "bytes and zoo.css")
