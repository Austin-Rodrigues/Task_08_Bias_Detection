# Task_08_Bias_Detection

Controlled experiment to detect prompt-framing and demographic effects in LLM-generated data narratives.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python src/experiment_design.py
# SIMULATION mode (no API keys needed):
python src/run_experiment.py
python src/analyze_bias.py
python src/validate_claims.py
```

Artifacts will appear in `results/` and `analysis/`.

### Using Real APIs (optional)
- Set `SIMULATION=false` and implement the `call_model(...)` adapter in `src/run_experiment.py` for each provider (Claude, GPT-4o, Gemini).
- Keep `data/` **out of git** (blocked by `.gitignore`).

## Structure
- `prompts/` — minimal-difference prompt templates (H1/H2/H3 conditions)
- `src/` — scripts for building prompt suite, running experiments, analysis, and basic claim validation
- `data/` — anonymized CSV (local only; **not committed**)
- `results/` — raw JSONL logs (optionally ignored)
- `analysis/` — scored outputs and summaries
- `streamlit_app.py` — optional dashboard

## Ethics & Compliance
- No PII. Use Player A–F.
- Record model, version, temperature, timestamps.
- Report null results as valid outcomes.
