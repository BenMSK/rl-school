# RL School, Korean mode: translation rules

The reader is a Korean speaker learning RL who will go on to read the English papers. So the prose is Korean and the
terms of art stay in English, exactly as they are written in the papers. "Bellman equation" is "Bellman equation", not "벨만 방정식".

## 1. What stays in English (Latin script, same spelling and capitalisation as the source)

- **Every RL/ML term of art.** agent, environment, state, action, reward, return, policy, value, value function,
  Q-value, discount factor, episode, trajectory, rollout, horizon, exploration, exploitation, greedy, ε-greedy, bandit,
  regret, MDP, Markov property, transition, dynamics, Bellman equation, backup, dynamic programming, policy evaluation,
  policy improvement, policy iteration, value iteration, Monte Carlo, temporal difference, TD error, TD target,
  bootstrapping, eligibility trace, on-policy, off-policy, Q-learning, SARSA, replay buffer, target network, function
  approximation, deadly triad, policy gradient, baseline, advantage, actor–critic, entropy, trust region, clipping,
  surrogate objective, KL divergence, importance sampling, model-based, model-free, world model, planning, latent,
  offline RL, behavior cloning, imitation learning, distribution shift, self-play, multi-agent, intrinsic reward,
  curiosity, reward model, reward hacking, fine-tuning, pretraining, prompt, token, sim-to-real, domain randomization,
  loss, gradient, gradient descent, learning rate, batch, minibatch, epoch, logit, softmax, overfitting, backpropagation,
  step, update, sample, sampling, noise, token, buffer, thread, worker, loop,
  and every other term a Korean ML researcher would say in English in a lab meeting. When unsure whether a word is a
  term of art, keep it in English.
- **Every proper noun**: people, labs, companies, products, models, algorithms, benchmarks, datasets, environments,
  paper and book titles, venue names (Sutton & Barto, DeepMind, AlphaGo, PPO, Atari, Montezuma's Revenge, NeurIPS).
  Never write names in Hangul.
- Symbols, formulas, variable names, code, URLs, units, file names.
- The lesson label "Day 7" (it is a link label) and the feature name "Paper Bible".

Attach Korean particles straight to the English word, chosen by how the word is pronounced:
policy를, reward가, state에서, agent는, return을, Q-learning은, value function이.

**Gloss once.** Where the English lesson defines a term (it is in `<strong>`), keep the term in English and, if it is a
common noun with a standard Korean word, add that word once in parentheses right after the closing tag:
`<strong>policy</strong>(정책)`, `<strong>reward</strong>(보상)`, `<strong>discount factor</strong>(할인율)`. After that
use the English term alone. No gloss for names (Bellman equation, Q-learning, Monte Carlo) and no gloss in papers,
quizzes, figures or widgets.

## 2. What becomes Korean

- All ordinary prose, and ordinary words that are not RL jargon: 학습, 훈련, 모델, 데이터, 알고리즘, 신경망, 확률,
  기댓값, 평균, 분산, 함수, 최적화, 파라미터, 시뮬레이션, 벤치마크, 아키텍처, 로봇, 게임, 실험, 논문, 연구.
- Field names: reinforcement learning → 강화학습 (the abbreviation RL stays), supervised learning → 지도학습,
  machine learning → 머신러닝, deep learning → 딥러닝.
- Everyday game names: Go → 바둑, chess → 체스, shogi → 쇼기.
- A verb or adjective used casually may be natural Korean ("the agent explores" → "agent가 탐색합니다"), but when the
  sentence is about the concept, use the term ("exploration과 exploitation의 균형").

## 3. Voice

- Lessons and papers: 합니다체 (…합니다, …입니다). Clear textbook Korean, short sentences. Translate the meaning, not
  the word order; no translationese (no "~에 의해", no stacked "~의 ~의", no "그것은").
- "Explain it to a 10-year-old" boxes: 해요체 (…예요, …해요), warm and simple, and still no jargon.
- Headings, table headers, labels, buttons: noun phrases without a sentence ending.
- Quotation marks around a passage quoted from a source: translate the passage into Korean and keep the quotation
  marks and the source chip. A famous phrase that is itself the point ("reward is enough", "the bitter lesson") stays
  in English, with the meaning in parentheses the first time.

## 4. Fixed wording (use exactly these)

| English | Korean |
|---|---|
| Week 1 · Day 3 | 1주차 · Day 3 |
| Day 3 (anywhere) | Day 3 |
| Q1. … / Answer 3. … | Q1. … / 정답 3. … |
| Notice: | 눈여겨볼 점: |
| Try it: | 직접 해 보기: |
| as of October 2026 | 2026년 10월 기준 |
| Figure 3 (of a paper) | Figure 3 |
| Systems view | 시스템 관점 |
| lesson / widget / quiz | 레슨 / 위젯 / 퀴즈 |
| paper review, entry | 논문 리뷰 |
| Reset / Step / Run / Play / Pause (buttons) | 초기화 / 한 step / 실행 / 재생 / 일시정지 |
| About 90 min · Needs Day 6 | 약 90분 · Day 6 필요 |
| Going deeper (optional): … | 더 깊이 (선택): … |
| Taught in Day 8 · Read time of the original: ~40 min | Day 8에서 다룸 · 원문 읽는 시간: 약 40분 |
| frame (of a game or video) | 프레임 (but "frame skip" stays) |
| this course | 이 코스 |
| Next → / ← Back | 다음 → / ← 이전 |
| Episodes / Steps (counters) | Episodes / Steps |

The headings that repeat in every lesson and paper ("Today's big idea", "Check yourself", "Sources", "The problem", …)
are already translated in `common.ko.txt`; they are not in your file.

## 5. Mechanics

- Numbers: keep every digit exactly as written (10,000 stays 10,000; 0.9 stays 0.9; 77.9% stays 77.9%). Number words
  may become digits or Korean (two → 두, one million → 100만).
- Dates: "25 Oct 2026" → "2026년 10월 25일".
- Tags: every tag of the English unit appears in the Korean unit, character for character (same attributes, same
  href). You may move a tag with its words to fit Korean word order. Never add, drop or edit a tag. Keep `&amp;`,
  `&lt;`, `&gt;` as entities.
- Source chips (`<a class="src" …>Author 2018</a>`) stay as they are and sit after the sentence they support.
- SVG labels (short units, often with `<tspan>`): room is tight. Hangul is about twice as wide as a Latin letter, so
  a Korean label should have at most about half as many characters as the English one. Most labels are terms and stay
  as they are.
- A unit that should stay exactly as in English: write `=` alone.
- `attr` units are plain text for screen readers (alt text, aria-label): no tags and no double quotes.
