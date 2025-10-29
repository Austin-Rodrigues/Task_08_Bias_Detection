# Oct 15 Progress Report — Task 08: Initial Planning

**Task Title:** Detecting Bias in LLM-Generated Data Narratives  
**Submission Date:** October 15, 2025  

---

## 1. Project Overview

This project aims to **design and execute a controlled experiment** to test whether **Large Language Models (LLMs)** generate biased narratives depending on how questions are framed or contextualized.

The study extends prior work on data storytelling by introducing systematic variations in prompts while keeping the dataset constant. The outcome will help evaluate **framing bias**, **demographic bias**, and **priming bias** in AI-generated analytical narratives.

---

## 2. Dataset and Domain

- **Dataset:** A small, anonymized dataset representing synthetic player performance statistics (Players A–F).  
- **Variables:** goals, assists, turnovers, minutes played, class year.  
- **PII Handling:** All identifiers are anonymized; no personal data or sensitive information is used.  
- **Storage:** Dataset kept locally under `data/players_anonymized.csv` and excluded from GitHub via `.gitignore`.

---

## 3. Research Questions / Hypotheses

| Hypothesis | Description | Independent Variable | Expected Bias Type |
|-------------|-------------|----------------------|--------------------|
| **H1: Framing Effect** | Compare positive vs. negative framing of the same question to see if sentiment shifts. | Prompt framing (positive / negative) | Valence bias |
| **H2: Demographic Mention** | Check if mentioning demographics (class year) changes which player receives recommendations. | Demographic info (on / off) | Demographic bias |
| **H3: Priming Bias** | Observe if priming the model about a player being “underperforming” affects evaluation outcomes. | Priming presence (yes / no) | Confirmation bias |

---

## 4. Experimental Design Plan

- **Controlled Variables:** Dataset, model temperature (0.2), and model version.  
- **Independent Variables (IVs):** Prompt framing, demographic mention, priming presence.  
- **Dependent Variables (DVs):** Sentiment polarity (VADER/TextBlob or fallback), response length, factual accuracy, and player recommendation frequency.  
- **Conditions:** 3 experiment families × 2 variations each = 6 prompt conditions.  
- **Repetitions:** 3 – 5 model runs per condition.  
- **Models:** Claude 3.5, GPT-4o (initially simulated, later real calls).

---

## 5. Planned Tools & Environment

- **Languages:** Python 3.13 (VS Code venv).  
- **Libraries:** `pandas`, `numpy`, `tqdm`, `vaderSentiment`, `textblob`, `matplotlib`.  
- **Structure:**  
  - `src/` → Python scripts (design, run, analyze, validate)  
  - `prompts/` → Conditioned templates  
  - `analysis/` → Results & summary outputs  
  - `.gitignore` → Blocks data/ and temp files  
- **Version Control:** Git + GitHub repository: *Task_08_Bias_Detection*

---

## 6. Planned Steps (Timeline)

| Week | Milestone | Target Date |
|------|------------|-------------|
| Week 1 (Oct 10 – 15) | Define hypotheses, dataset, and prompt templates | ✅ Oct 15 |
| Week 2 (Oct 16 – 31) | Implement scripts, simulation pipeline, run test outputs |  |
| Week 3 (Nov 1) | Submit design + collection progress (Nov 1 report) |  |
| Week 4 (Nov 2 – 15) | Switch to real LLMs, run full trials, analyze bias patterns |  |
| Week 5 (Nov 15) | Submit final report and code |  |

---

## 7. Expected Deliverables

- Python pipeline for prompt generation, run logging, and analysis.  
- Bias metrics (sentiment, factuality, selection frequency).  
- Reports for **Nov 1** and **Nov 15** milestones.  
- Final GitHub repository (public, code-only).

---

## 8. Ethical and Compliance Notes

- No PII or real-world identities used.  
- Datasets are synthetic and locally stored.  
- GitHub excludes `data/` and intermediate results.  
- Follows Syracuse University’s OPT Research compliance requirements.

---

**Current Status (as of Oct 15):**  
Initial planning completed, dataset prepared, hypotheses defined, repository scaffolded (`Task_08_Bias_Detection` created in VS Code and ready for version control).  
Next: Implement experiment design and simulation pipeline for Nov 1 progress report.
