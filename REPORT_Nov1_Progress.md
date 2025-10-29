# NOV 1 Progress Report — Task 08 (Experimental Design & Data Collection)

**Summary since Oct 15:** Repo scaffolded, hypotheses pre-registered, prompt suite generated, logging implemented, and initial runs completed (simulation mode to validate pipeline).

## Experimental Design
- **Dataset:** Anonymized season stats (Players A–F).
- **IVs:** Framing (positive/negative), Demographic mention (on/off), Priming (present/absent).
- **DVs:** Sentiment (VADER/TextBlob), recommendation types, stat reference counts.
- **Controls:** Temperature=0.2, same data block, same model version recorded, 3 samples per prompt.

## Prompt Conditions
H1: Positive vs Negative  
H2: Demographics vs None  
H3: Primed vs Unprimed

## Data Collection
- Mode: **Simulation** to verify pipeline end-to-end (no API keys).  
- Runs: 6 conditions × 2 models × 3 samples = **36** records (increase as needed).  
- Logged fields: timestamp, model, temperature, family, condition, prompt text, data hash, response text, run_id.

## Preliminary Analysis (Simulation)
- Sentiment means diverge by framing as expected; files in `analysis/summary_by_condition.csv`.
- No claim mismatches in synthetic responses (validator included).

## Next Steps (Week of Oct 28–Nov 3)
- Swap to real LLM calls (Claude via SU enterprise; GPT-4o; Gemini).  
- Expand to 5 samples/condition, add χ²/t-tests and effect sizes.  
- Begin visualizations and draft Bias Catalogue.

## Compliance
- `.gitignore` blocks `data/` and large results.
- No PII; only anonymized synthetic data.
