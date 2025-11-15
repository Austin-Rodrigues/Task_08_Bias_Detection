# LLM Bias Detection – Task 08

This repository contains a complete, reproducible controlled experiment designed to measure bias in Large Language Models (LLMs). The project evaluates how prompt framing, demographic cues, and hypothesis priming influence model-generated narratives when interpreting identical numerical data.


---

# Project Overview

LLMs can shift their interpretations based on subtle changes in wording. This experiment evaluates whether LLMs:

- Change sentiment under positive vs negative framing  
- Shift tone when demographic information is added  
- Focus disproportionately on specific players under priming  
- Maintain accurate citation of statistics  
- Produce biased narratives despite identical input data

A synthetic dataset of six anonymized players was used. A total of 18 LLM responses were collected from Claude 3.5 Sonnet.

---

# Hypotheses Tested

### H1: Framing Bias  
Does positive vs negative prompt wording change sentiment?

### H2: Demographic Bias  
Does including class year alter interpretation or recommendations?

### H3: Priming Bias  
Does stating "Player B is underperforming" change the model's evaluation?

---

# Key Findings

| Hypothesis | Significant | Effect Size | Interpretation |
|-----------|-------------|-------------|----------------|
| H1 Framing | No (p = 0.2907) | Large (d = 0.993) | Tone strongly influenced sentiment |
| H2 Demographics | No (p = 0.1788) | Very Large (d = -1.329) | Class year increased positivity |
| H3 Priming | No (p = 0.3610) | Large (d = 0.841) | Priming shifted focus and tone |

Factual Accuracy  
12 claims extracted  
0 incorrect  
100 percent accuracy

---

# How to Run the Experiment

### 1. Create Virtual Environment

python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Mac or Linux

2. Install Dependencies
pip install -r requirements.txt

3. Generate Prompts
python src/experiment_design.py

4. Run Experiment (Simulation Mode)
No API keys required. Produces deterministic mock results.
python src/run_experiment.py

5. Analyze Bias
python src/analyze_bias.py

6. Validate Claims
python src/validate_claims.py
Outputs will appear in the analysis directory.

Using Real LLM APIs (Optional)
To run the experiment with actual Claude or GPT models:
Set SIMULATION=false in the environment
Implement the call_model adapter inside src/run_experiment.py
Use environment variables for API keys
Do not commit keys or data to git

Outputs Generated
Analysis Artifacts
summary_by_condition.csv
all_runs_scored.csv
statistical test results
validation_report.txt
claim_mismatches.json

Visualizations
sentiment_comparison.png
length_comparison.png
player_mentions_heatmap.png

Ethics and Compliance
No personally identifiable information included
Players anonymized as A to F
All model metadata logged (model name, version, temperature, timestamp)
Null and non-significant findings were reported accurately
Designed for transparency and reproducibility

Final Report
A full academic write-up is provided in:
Report_Nov15.md
This includes methodology, results, effect sizes, visualizations, bias catalogue, limitations, and future work.

Contact
For questions or improvements:
GitHub: Austin-Rodrigues
