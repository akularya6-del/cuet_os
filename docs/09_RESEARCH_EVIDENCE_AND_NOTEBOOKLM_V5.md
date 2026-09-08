# 09_RESEARCH_EVIDENCE_AND_NOTEBOOKLM_V5

**No unverified AI claim becomes canonical truth.** Funnel, evidence law, and NotebookLM contract carried from V4; capture mechanics re-bound to Codex-verified capabilities.

---

## 1. The research funnel (9 stages, each with an owner)

```
Q QUESTION (user or watchlist trigger; VOI gate first)
→ S SEARCH (Codex web search — cached default, --search live [OFFICIAL VERIFIED];
   free tools when sufficient)
→ P PRIMARY SOURCES (prefer official: NTA, DU, Google/OpenAI/Anthropic/DeepSeek
   official docs; never accept a blog's claim about what an official page says)
→ C CAPTURE (page content → research/sources/ with URL, date, sha; fetch MCP or
   scripted curl; Codex reads the capture, not the live page, so evidence is stable)
→ X EXTRACTION (T2 via scripts: structured JSON of dates, numbers, rules, quotes+refs)
→ Y CHEAP SYNTHESIS (T2/T3 draft summary with per-claim source refs)
→ Z CROSS-CHECK (second engine OR direct primary re-read for load-bearing claims)
→ CL CLAIM REGISTRY (claim → evidence tag → sources → expiry clock)
→ M MEMORY (only canonized claims may drive strategy; ledgers updated via scripts)
```

VOI gate (value-of-information, carried from V4): before any research task, one line — decision it changes, cost if wrong, cost to research. "Interesting" is not a gate pass.

## 2. Evidence tag law (mandatory everywhere in the OS)

| Tag | Meaning | May drive strategy? |
|---|---|---|
| [OFFICIAL VERIFIED date] | read on official source by the OS on that date | yes, until clock expires (01 §5) |
| [HISTORICAL OFFICIAL] | official, but for a prior cycle | as baseline only, flag REQUIRES-CONFIRMATION |
| [SECONDARY date] | reputable independent source | 2 independent supports to promote to strategy use |
| [INFERENCE] | OS conclusion from tagged inputs | only with named inputs; review monthly |
| [ESTIMATE] | arithmetic from tagged numbers | for budgets only; verify on first real bill |
| [UNKNOWN] | not verifiable today | never drives anything; gets a verification task |
| [REQUIRES 2027 CONFIRMATION] | cycle-specific | frozen until NTA/DU 2027 documents land |

Fabrication is the cardinal sin of this OS: a fabricated quota, price, date, or catalog entry is treated as a system defect with a root-cause note in the monthly audit (13 §2-A12).

## 3. Source registry & clocks

`research/sources/` — one file per capture (front-matter: URL, publisher, captured date, sha256, access path used). `research/claims.md` — claim registry with tags and refresh clocks (30-day for prices/quotas; cycle-locked for exam rules). Claim lifecycle: proposed → supported (≥1 tag) → canon (drives logic) → stale (clock expired → demoted to UNKNOWN until re-verified). `research/watchlist.md` — W-items with check dates: W1 NTA 2027 notification+syllabus (~Dec 2026–Feb 2027 [UNKNOWN]) · W2 DU CSAS 2027 bulletin · W3 Gemini free-tier promo end (2026-12-31 [OFFICIAL]) · W4 GCP credit expiry dates (per account, from console) · W5 Codex plan/quota changes · W6 Gemini 3.x price tiers · W7 Claude price moves · W8 NotebookLM limit changes (2026-09-02 change precedent [OFFICIAL support page]) · W9 DeepSeek peak-season pricing · W10 OpenRouter free-tier terms · W11 Antigravity plan changes · W12 MCP spec/server deprecations · W13 NIOS PE practical dates · W14 FX drift (>5% triggers budget recompute).

## 4. NotebookLM contract (the citation-bound librarian)

**NotebookLM CAN DO (N1–N7):** N1 hold the canonical *copies* of official sources (NTA notices, DU bulletins, NIOS material, subject references) with grounded citations; N2 generate study guides, briefs, timelines **from those sources only**; N3 flashcard/quiz seeds (daily caps: 20/day reports+quiz family, 6/day video [TIER A V4]; plan changes from 2026-09-02 [OFFICIAL support page] — recheck monthly); N4 source comparison ("what does NTA say vs coaching PDF"); N5 knowledge transformation (FAQ → Q&A; syllabus → topic list, human-verified before import to subjects.json); N6 audio/video overviews for passive review (3/day audio [TIER A V4]); N7 citation-checked answers with quotes.

**NOTEBOOKLM MUST NOT DO:** be the canonical strategy authority (that's ledgers + reviews); be the memory system; be cited as evidence without the underlying source being captured in research/sources/; feed exam rules (it can hallucinate around dated/ambiguous sources; NTA notification governs); replace bank validation (its quizzes are seeds, not assessments); hold anything sensitive (data class PERSONAL+ — 13 §4).

Notebook structure (8, carried from V4): NB-NTA · NB-DU · NB-SUBJECTS(x5 or grouped) · NB-NIOS-PE · NB-STRATEGY(cut decisions only) · NB-BUSINESS · NB-ARCHIVE. Limits for the free/Standard tier: 100 notebooks, 50 sources/notebook, 500k words/source, ~50 chats/day [TIER B multiple 2026]; **no official API exists** [VERIFIED via continued community complaints, 2026-09] — all interaction is manual/UI.

MCP status: community NotebookLM MCP servers exist (browser-cookie or unofficial-API based) [TIER B mcpservers.org/github 2026]. Verdict unchanged from V4: **TRUST 3, OPTIONAL, never load-bearing, never logged into with the primary Google account session** — cookie-automation against your real account risks the account itself. If one is ever trialed: burner profile, read-only use, zero personal data, immediate removal on any anomaly (10 §2).

## 5. Research budgets

Codex interactive research: ≤2 live-search sessions/day (quota care), each ≤15 min. Deep-research-style tasks (premium) require VOI ≥ 48 and happen at most weekly. T2 extraction is unmetered within nightly batches. Any research that starts costing credits → 11 §7 gate. Research that produces nothing citable in 45 minutes is abandoned (sunk-cost law) and logged as a watchlist item for later.

## 6. Canonization protocol (the only path into strategy)

Load-bearing claim → (1) primary source captured; (2) extraction schema-validated; (3) cross-check passes (second engine or direct re-read); (4) evidence tag assigned with date; (5) claim registry updated; (6) affected configs/ledgers updated by script; (7) if the claim contradicts an existing canon claim, the old one is superseded (never edited) with a note. Anything skipped in this chain stays [UNKNOWN] and may inform but never decide.
