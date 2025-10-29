import json
from pathlib import Path
import pandas as pd

# Optional imports; provide fallbacks if unavailable
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except Exception:
    SentimentIntensityAnalyzer = None

try:
    from textblob import TextBlob
except Exception:
    TextBlob = None

POS_WORDS = set("opportunity growth strong promising improvement breakthrough".split())
NEG_WORDS = set("poor concern underperforming mistake issue weak problem".split())

def fallback_sentiment(text: str) -> float:
    words = [w.strip(".,;:!?()").lower() for w in text.split()]
    pos = sum(1 for w in words if w in POS_WORDS)
    neg = sum(1 for w in words if w in NEG_WORDS)
    if pos + neg == 0:
        return 0.0
    return (pos - neg) / (pos + neg)

def main():
    path = Path("results/outputs.jsonl")
    if not path.exists():
        raise SystemExit("No results/outputs.jsonl found. Run src/experiment_design.py then src/run_experiment.py first.")
    rows = []
    vs = SentimentIntensityAnalyzer() if SentimentIntensityAnalyzer else None
    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        txt = r["response_text"]
        if vs:
            vader_val = vs.polarity_scores(txt)["compound"]
        else:
            vader_val = fallback_sentiment(txt)
        if TextBlob:
            tb_val = TextBlob(txt).sentiment.polarity
        else:
            tb_val = fallback_sentiment(txt)
        rows.append({
            "model": r["model"],
            "prompt_family": r["prompt_family"],
            "condition": r["condition"],
            "run_id": r["run_id"],
            "vader_compound_or_fallback": vader_val,
            "textblob_polarity_or_fallback": tb_val,
            "len_chars": len(txt)
        })
    df = pd.DataFrame(rows)
    Path("analysis").mkdir(exist_ok=True)
    df.to_csv("analysis/all_runs_scored.csv", index=False)
    g = df.groupby(["prompt_family","condition"]).agg(
        n_runs=("run_id", "count"),
        vader_mean=("vader_compound_or_fallback","mean"),
        vader_std=("vader_compound_or_fallback","std"),
        tb_mean=("textblob_polarity_or_fallback","mean"),
        tb_std=("textblob_polarity_or_fallback","std"),
        len_mean=("len_chars","mean")
    ).reset_index()
    g.to_csv("analysis/summary_by_condition.csv", index=False)
    print("Saved analysis/all_runs_scored.csv and analysis/summary_by_condition.csv")
    print(g)

if __name__ == "__main__":
    main()
