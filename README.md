# RL School

A two-week, plain-English course on reinforcement learning, from rewards and bandits to world models, RL-trained reasoning models, agentic RL and robots (as of October 2026). It also has a "Paper Bible" of 20 landmark papers, each explained three ways: in one sentence, for a 10-year-old, and step by step. It is one self-contained web page with 29 interactive widgets, an architecture diagram for every method, 144 quiz questions, and a source link on every claim.

| Where | URL | Notes |
|---|---|---|
| GitHub Pages | https://benmsk.github.io/rl-school/ (not published yet) | Progress (days done) and theme are saved only in the browser. Add it to the iPhone home screen for an app icon. |
| Local | double-click `index.html` | Works offline except Google Fonts. |

Built with the `school` skill (`~/.claude/skills/school`), in the same house style as [LLM School](https://benmsk.github.io/llm-school/). The research notes are in `../RL_school_research/` (one per 2–3 days, every source URL, an "Unverified / caution" list at the end of each). They sit outside this folder so they are not published.

## Files

```
RL_school/                  ← git root (github.com/BenMSK/rl-school, branch main; not created yet)
├─ index.html               ← the whole site: CSS + content + script. The only source.
├─ apple-touch-icon.png     ← iOS home-screen icon 180px (loop arrow + reward star)
├─ icon-192.png, icon-512.png, manifest.webmanifest   ← Android / PWA icon and manifest
├─ img/papers/*.png         ← 23 figures reproduced from the reviewed papers (≤1400px wide, <200 KB)
├─ .nojekyll                ← GitHub Pages serves files as-is
├─ tools/htmlcheck.js       ← tag balance + quiz answer range + every widget defined + no duplicate ids
├─ tools/review.py          ← audit and screenshot every diagram/widget of one lesson   python tools/review.py d8
├─ tools/makeicon.js        ← icon rasterizer (ICON spec matches the header logo)       node tools/makeicon.js .
├─ tools/figcrop.py         ← crops "Figure N" out of a paper PDF (needs pymupdf)       python tools/figcrop.py paper.pdf 2 out.png
└─ README.md
```

## Inside index.html

- `<head>`: meta, icons, manifest, Google Fonts (Inter, Space Grotesk, JetBrains Mono), one `<style>` block. The design tokens live in `:root` (teal skin) and are redefined for dark mode twice: under `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`, and under `:root[data-theme="dark"]` for the toggle. Every text/background pair is at least 4.5:1.
- `<header class="top">`: brand, version `v1.x (date)`, theme button, two tabs.
- `.pane[data-pane=course]`: day chips (built by script), `#d0` overview (hero, how-to, syllabus table built from the day headers, box legend), then `section.day[data-day=1..14]`.
- `.pane[data-pane=papers][data-lib]`: library hero, tag filter and cards (built by script from the entries), then `article.entry#p-…[data-year][data-tags]`.
- `<script id="data" type="application/json">`: `timeline` (36 dated milestones) and `bench` (Atari median, AIME, LIBERO) for the Day 14 widgets.
- `<script>`: config (`LS="rl-school"`, `WEEK`, `T` UI strings), theme, routing (`#d7`, `#papers`, `#p-ppo`), progress, quiz handling, phone table-to-card labels, `lineChart` and `stepper` helpers, the `VIZ` registry (one function per widget), and `fitText`. That last one shrinks an SVG label that overflows its box or the canvas (to 70% at most), shifts labels back inside the edge, and paints free-standing labels on top with a halo. It runs on every navigation, after web fonts load, and after any widget redraw, because label widths differ by device and font.

### Content conventions

- Every claim worth checking carries a source chip `<a class="src" href="…">Author Year</a>` linking to the primary source (Sutton & Barto, arXiv, Nature, official docs and blogs).
- Lesson structure: `header.day-h` → `.box.key` → numbered `h3` sections with widgets (`div.viz`) and inline-SVG figures → `.box.tip` / `.kid` / `.dont` / `.note` → an **Architecture** section (diagram of the components and what flows between them, then a "Systems view" note) → `.quiz` (`.q[data-a=index]`, four `.opt`, hidden `.exp`) → `.box.ok` recap → `.refs` → `p.next`.
- Paper structure: header → in one sentence → for a 10-year-old → problem → key idea → how it works (with the architecture) → results → why it mattered → limitations → how to read the paper → quiz → references.
- Inline SVG uses only CSS-variable colours, so it works in both themes. Widget numbers are real, seeded computations, and the prose quotes what the widget produces.
- Replicated numbers (10-armed testbed, random walk RMS, cliff walking) are labelled as replications, not book figures.
- Widget names (all in `VIZ`): gridworld, discount, bandit, ucb, mdp, bellman, dp, gpi, td, trace, qlearn, dqn, pg, gae, ppo, sac, dyna, imagine, offline, denoise, explore, selfplay, rlhf, grpo, agentrl, sim2real, vla, timeline, bench.
- Day ids `d1`…`d14` and paper ids `p-…` are link targets. Do not rename them.

## Editing and publishing

1. Edit `index.html`.
2. `node tools/htmlcheck.js index.html` → must print `errors: 0`.
3. If you changed a diagram or widget: `python tools/review.py d8` (or `p-dqn`). It lists labels that run off the canvas, overlap another label, or are crossed by a line, and screenshots each diagram. Known, intentional findings: the paired arrows in `qlearn` (both agents' paths) and the crossed-out "value model" in Day 12.
4. If you changed the script, open the page in a browser and check the console.
5. Bump the version in the header `.ver` span and in the footer, and add a line to the change log below.
6. `git add -A && git commit -m "…" && git push` → live in 1–2 minutes (after the repo and Pages are set up).
7. To change the icon: edit the `<svg class="logo">` in the header and the matching `ICON` shapes in `tools/makeicon.js`, run `node tools/makeicon.js .`, then on the phone remove and re-add the home-screen icon.

## Change log

| Date | Version | Git tag | What |
|---|---|---|---|
| 2026-10-25 | v1.0 | – | First release. 14 lessons (Week 1: what RL is, bandits, MDPs and Bellman equations, dynamic programming, Monte Carlo and TD, Q-learning/SARSA/DQN, policy gradients and actor–critic; Week 2: TRPO/PPO/SAC, model-based RL and world models, offline RL and generative policies, exploration/self-play/multi-agent, RL for language models and agents, RL in the wild, the frontier and open problems). 20 paper reviews with 23 figures from the papers. 29 widgets, an architecture diagram per method, 144 quiz questions. Light/dark theme, phone layout, home-screen icon and manifest. |

## Known gaps and things to re-check later

- Fast-moving facts (reasoning-model scores, frontier-lab statements, robot results) are stated "as of October 2026" and will age. Day 12, Day 14, and the `timeline` and `bench` data are the first places to refresh.
- openai.com returned 403 during research, so OpenAI's own blog numbers are not used: o1 is cited through its system card and DeepSeek-R1's tables. OpenAI Five uses only the arXiv paper's figures (not the blog's "45,000 years" or "180 years per day"). No o3/GPT-5 AIME numbers appear.
- The AIME 2026 rows in the `bench` widget come from a secondary mirror of MathArena and are marked "secondary" in the chart, table and prose.
- Only the 2026 statements that could be opened are used: DeepSeek-V4 (24 Apr 2026) and Anthropic's Opus 5.5 post (22 Sep 2026). No OpenAI or Google DeepMind 2026 RL text is cited.
- Williams 1992 (REINFORCE) could not be opened and is cited through Sutton & Barto. The Nature DQN hyperparameters (C = 10,000, lr 0.00025) and per-game scores come from the Double DQN paper's restatement, because the Nature extended-data tables are images.
- DeepSeek-R1: v1 (71.0% AIME for R1-Zero) and v2/Nature (77.9%) numbers are both given and attributed to their version. Distillation numbers come from the v1 HTML.
- Dreamer 4's "17 tasks" comes from the project page. "32×32 categoricals" is confirmed for DreamerV2 and assumed for V3. Diffusion Policy's task count varies by paper version (11/12/15); the +46.9% average does not.
- Cicero numbers come from Meta's pages, Go-Explore numbers from arXiv v1, and AlphaChip's per-TPU-generation claims from Google's blog (the Cheng/Kahng critique is presented alongside).
- The DeepMind data-centre cooling posts describe prediction plus optimisation, not RL. Day 13 says so and uses them as a lesson in reading claims.
- InstructGPT's numeric β is not given in the paper text that was read, so the `rlhf` widget's β = 0.05 is labelled illustrative. The "NeurIPS 2022/2023" venues for InstructGPT and DPO come from general knowledge, not the arXiv pages.
- Figure numbering follows the arXiv version used for each crop. If a paper is revised, re-check the numbers.
