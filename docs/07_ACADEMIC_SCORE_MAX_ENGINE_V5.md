# 07_ACADEMIC_SCORE_MAX_ENGINE_V5

**The academic core.** Carried from V4 with bindings re-pointed to Codex; the learning science, mathematics, and gates are unchanged because they were engine-independent. Config-driven for CUET-2027 uncertainty.

---

## 1. What the engine optimizes

Expected marks under the official scheme — `config/marking_scheme.json` (2026 baseline: **+5 correct, −1 wrong, 0 unanswered** [TIER B multiple 2026 sources]; 2027 values UNKNOWN → set at NTA notification; the JSON, not this document, is the truth). Optimization levers, in order of measured leverage: error elimination → accuracy under time → question recognition (pattern exposure) → coverage of high-yield topics → retention stability → guess discipline. The engine allocates time by **expected score gain per hour**, never by equal treatment or by what is interesting.

## 2. Subject slate (locked earlier; carried)

English (core) · Mathematics (weakest, 0/10 baseline) · Chemistry · General Aptitude Test (0/10 baseline) · **Physical Education as NIOS 5th subject (paper code 321 [HISTORICAL OFFICIAL 2026], locked decision — CS and Home Science remain rejected)**. DU-target programs set the target band: SC composite ~630–670 [HISTORICAL OFFICIAL 2026]; re-verify per cycle. `config/subjects.json` holds per-subject: exam weight, current baseline, target, chapter list, NIOS/PE specifics (theory + practical journal), and priority class.

## 3. Time allocation (≈865 h to exam, Sep 2026 → May 2027)

V4 allocation stands as the prior: Maths 250 · GAT 230 · Chemistry 130 · English 120 · PE 55 · Mocks+analysis 80. `scripts/allocator.py` recomputes the **remaining** split monthly from ledgers: `hours(topic) ∝ expected_score_gain(topic) / (mastery(topic) + 0.15)` with floor/ceiling per subject class. GAT and Maths own the biggest shares because their baselines are lowest (maximum gain per hour). PE is deliberately thin — high marks-per-hour, low variance, don't gold-plate it.

## 4. Expected-score-gain priority function (verbatim mechanism from V4)

```
EXPECTED_SCORE_GAIN = W1·GAP_WEIGHT      # marks currently lost on this topic cluster
                    × W2·FREQUENCY       # exam frequency 1–5 (past papers + blueprint)
                    × W3·LEARNABILITY    # 1–5 inverse difficulty for THIS student
                    × W4·RETENTION_COST  # decay risk multiplier
                    × W5·PREREQ_WEIGHT   # unlocks downstream topics 0.5–1.5
```
Weights live in `config/budget.json`; scripts compute; Codex reads the ranked list and proposes the day's target. Human sanity-check: if the list ever contradicts common sense (e.g., "ignore PE entirely"), the weights are wrong — fix weights, not intuition.

## 5. Error taxonomy (closed 10-class set; every wrong answer gets exactly one code)

E1 concept-gap · E2 method-selection · E3 calculation-slip · E4 misread-question · E5 option-trap · E6 time-pressure abandon · E7 guess-wrong · E8 overconfidence (knew, skipped practice) · E9 recall-fail (had it, lost it) · E10 transcription/OMR. Scripts assign tentative codes from the correction pattern (T2 classifier on unstructured notes); Codex confirms ambiguous cases at REVIEW. **Careless-cluster guard:** E3+E4+E10 ≥ 40% of a week's errors → the intervention is procedure (checklists, marking discipline), not more content — the OS states this explicitly so "study more" never gets prescribed for a precision problem. **Guess-rate guard:** E7 share rising → timing strategy review, since +5/−1 makes blind guessing negative-EV; partial-elimination guessing stays positive-EV.

## 6. Mastery gates R1/R2 (deterministic; carried from V4)

| Gate | Requirement | Consequence of pass |
|---|---|---|
| **R1 (learned)** | ≥85% accuracy on ≥15 fresh questions, drawn from bank only, no notes | topic leaves "active learning"; enters spaced maintenance |
| **R2 (installed)** | R1 criteria repeated ≥48 h later, mixed with 2 other topics (interleaving), timed | topic enters long-horizon decay probes; prerequisite for "protected" status |

Gates are computed by `scripts/mastery.py` from ledgers — no AI judgment anywhere in the pass/fail path. Failed gate → topic re-enters active queue with the failure mode (accuracy vs speed vs mixed-interference) recorded.

## 7. Retention & decay system

Spaced schedule via `scripts/scheduler.py` (FSRS-style intervals: 1/3/7/14/30/60 days, adjusted by recall grade). Decay probes are 5-question micro-quizzes pulled from bank at scheduled intervals; passing keeps the interval, failing halves it and re-queues the topic. **14-days-without-contact rule:** any topic unseen for 14 days gets an automatic probe in the next drill window (01 §5 clock). Retention is measured, not assumed — the exam is in ~8 months; September learning is worthless if it evaporates by March.

## 8. Speed and exam-craft

Per-section timing budgets from `config/subjects.json` (recomputed after each mock). Drills: timed sets at 1.15× exam pace, then at 1.0×. Question-recognition training: tag each practiced question with its recognition cue (e.g., "sees discriminant → think factor or formula"); bank queries can then drill "show 10 stems, name the cue" — cheap, brutal, effective. OMR discipline uses the E10 checklist. Guess policy: attempt iff ≥2 options eliminated (positive EV under +5/−1); otherwise leave. All exam-craft rules are re-derived if the 2027 marking scheme changes (§1).

## 9. Future-impact horizons (1/3/7/14/30 days + final phase)

Every high-value decision (skip a chapter, double GAT hours, add a second mock/week) logs a horizon estimate at decision time: immediate effect, retention effect, prerequisite effects, downstream score impact, opportunity cost, reversibility, risk. `scripts/horizons.py` resurfaces the 3/7/14/30-day predictions on schedule and the REVIEW compares prediction vs reality — this is how the system (and the student) calibrates judgment over months (12 §2 consumes the same data).

## 10. What this engine refuses to do

No "study everything equally." No new content in the last 10 days. No timetable the user didn't co-sign. No strategy change off one mock (12 §3 thresholds). No PE neglect despite it being "easy" (it's 1/5 of the slate and the cheapest marks). No chapter skipped without a horizon note. No trusting any AI's claim about the 2027 pattern — the NTA notification is the only authority (06 §5).
