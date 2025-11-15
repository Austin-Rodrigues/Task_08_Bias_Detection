"""
analyze_bias.py
Quantitative analysis of LLM outputs.
Measures: sentiment, player mentions, recommendation types, response length.
Outputs: analysis/all_runs_scored.csv, analysis/summary_by_condition.csv
"""

import json
import re
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

# Sentiment analysis
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except:
    VADER_AVAILABLE = False
    print("⚠️  VADER not available, using fallback")

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except:
    TEXTBLOB_AVAILABLE = False
    print("⚠️  TextBlob not available, using fallback")

# Sentiment word lists
POS_WORDS = set([
    "opportunity", "growth", "strong", "promising", "improvement", "breakthrough",
    "potential", "excellent", "outstanding", "effective", "successful", "solid",
    "impressive", "develop", "enhance", "optimize", "strength", "advantage"
])

NEG_WORDS = set([
    "poor", "concern", "underperforming", "mistake", "issue", "weak", "problem",
    "struggling", "deficient", "inadequate", "lacking", "correction", "needs",
    "shortcoming", "limitation", "deficit", "flaw", "error"
])


def fallback_sentiment(text: str) -> float:
    """Fallback sentiment scorer when VADER unavailable"""
    words = [w.strip(".,;:!?()[]\"'").lower() for w in text.split()]
    pos = sum(1 for w in words if w in POS_WORDS)
    neg = sum(1 for w in words if w in NEG_WORDS)
    if pos + neg == 0:
        return 0.0
    return (pos - neg) / (pos + neg)


def extract_player_mentions(text: str) -> dict:
    """Count mentions of each player"""
    counts = {}
    for player in ['A', 'B', 'C', 'D', 'E', 'F']:
        # Match "Player A", "player A", or standalone "A" in context
        pattern = rf'\b[Pp]layer\s+{player}\b|\b{player}\b'
        counts[player] = len(re.findall(pattern, text))
    return counts


def classify_recommendation_type(text: str) -> dict:
    """
    Classify recommendation types mentioned in response.
    Categories based on task requirements.
    """
    text_lower = text.lower()

    types = {
        'defensive': 0,
        'offensive': 0,
        'individual': 0,
        'team': 0,
        'technical': 0,
        'strategic': 0
    }

    # Defensive keywords
    if any(word in text_lower for word in ['defense', 'defensive', 'protect', 'guard', 'prevent']):
        types['defensive'] = 1

    # Offensive keywords
    if any(word in text_lower for word in ['offense', 'offensive', 'attack', 'score', 'goal']):
        types['offensive'] = 1

    # Individual focus
    if any(word in text_lower for word in ['individual', 'personal', 'one-on-one', 'player-specific']):
        types['individual'] = 1

    # Team focus
    if any(word in text_lower for word in ['team', 'group', 'collective', 'together', 'coordination']):
        types['team'] = 1

    # Technical skills
    if any(word in text_lower for word in ['technique', 'skill', 'drill', 'practice', 'training']):
        types['technical'] = 1

    # Strategic
    if any(word in text_lower for word in ['strategy', 'tactical', 'decision', 'positioning', 'awareness']):
        types['strategic'] = 1

    return types


def main():
    path = Path("results/outputs.jsonl")
    if not path.exists():
        raise SystemExit("❌ No results/outputs.jsonl found.\n"
                         "   Run: python src/run_experiment.py --convert")

    print("Analyzing LLM responses...")
    print(f"Sentiment: {'VADER' if VADER_AVAILABLE else 'Fallback'}")
    print(f"Polarity: {'TextBlob' if TEXTBLOB_AVAILABLE else 'Fallback'}\n")

    rows = []
    vs = SentimentIntensityAnalyzer() if VADER_AVAILABLE else None

    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        txt = r["response_text"]

        # Sentiment scores
        if vs:
            vader_scores = vs.polarity_scores(txt)
            vader_val = vader_scores["compound"]
            vader_pos = vader_scores["pos"]
            vader_neg = vader_scores["neg"]
        else:
            vader_val = fallback_sentiment(txt)
            vader_pos = vader_neg = None

        if TEXTBLOB_AVAILABLE:
            blob = TextBlob(txt)
            tb_val = blob.sentiment.polarity
            tb_subj = blob.sentiment.subjectivity
        else:
            tb_val = fallback_sentiment(txt)
            tb_subj = None

        # Player mentions
        mentions = extract_player_mentions(txt)

        # Recommendation types
        rec_types = classify_recommendation_type(txt)

        # Response characteristics
        words = txt.split()
        sentences = txt.split('.')

        rows.append({
            "model": r["model"],
            "model_provider": r.get("model_provider", "Unknown"),
            "prompt_family": r["prompt_family"],
            "condition": r["condition"],
            "run_id": r["run_id"],

            # Sentiment metrics
            "vader_compound": vader_val,
            "vader_pos": vader_pos,
            "vader_neg": vader_neg,
            "textblob_polarity": tb_val,
            "textblob_subjectivity": tb_subj,

            # Response metrics
            "len_chars": len(txt),
            "len_words": len(words),
            "len_sentences": len([s for s in sentences if s.strip()]),

            # Player mentions
            "mentions_A": mentions['A'],
            "mentions_B": mentions['B'],
            "mentions_C": mentions['C'],
            "mentions_D": mentions['D'],
            "mentions_E": mentions['E'],
            "mentions_F": mentions['F'],
            "total_mentions": sum(mentions.values()),

            # Recommendation types
            "rec_defensive": rec_types['defensive'],
            "rec_offensive": rec_types['offensive'],
            "rec_individual": rec_types['individual'],
            "rec_team": rec_types['team'],
            "rec_technical": rec_types['technical'],
            "rec_strategic": rec_types['strategic'],
        })

    df = pd.DataFrame(rows)
    Path("analysis").mkdir(exist_ok=True)

    # Save detailed results
    df.to_csv("analysis/all_runs_scored.csv", index=False)
    print(f"✓ Saved analysis/all_runs_scored.csv ({len(df)} responses)")

    # Summary by condition
    g = df.groupby(["prompt_family", "condition"]).agg(
        n_runs=("run_id", "count"),
        vader_mean=("vader_compound", "mean"),
        vader_std=("vader_compound", "std"),
        tb_mean=("textblob_polarity", "mean"),
        tb_std=("textblob_polarity", "std"),
        len_mean=("len_chars", "mean"),
        words_mean=("len_words", "mean"),
        mentions_mean=("total_mentions", "mean"),
    ).reset_index()

    g.to_csv("analysis/summary_by_condition.csv", index=False)
    print(f"✓ Saved analysis/summary_by_condition.csv")
    print("\n" + "="*80)
    print("SUMMARY BY CONDITION")
    print("="*80)
    print(g.to_string(index=False))

    # Statistical tests as required
    print("\n" + "="*80)
    print("STATISTICAL TESTS")
    print("="*80)

    # H1: Framing effect
    h1_pos = df[(df.prompt_family == "H1_framing") & (
        df.condition == "positive")]["vader_compound"]
    h1_neg = df[(df.prompt_family == "H1_framing") & (
        df.condition == "negative")]["vader_compound"]

    if len(h1_pos) > 1 and len(h1_neg) > 1:
        t_stat, p_val = stats.ttest_ind(h1_pos, h1_neg)
        pooled_std = np.sqrt((h1_pos.std()**2 + h1_neg.std()**2) / 2)
        effect_size = (h1_pos.mean() - h1_neg.mean()) / \
            pooled_std if pooled_std > 0 else 0

        print(f"\n📊 H1: Framing Effect (Positive vs Negative)")
        print(
            f"   Positive: M={h1_pos.mean():.3f}, SD={h1_pos.std():.3f}, n={len(h1_pos)}")
        print(
            f"   Negative: M={h1_neg.mean():.3f}, SD={h1_neg.std():.3f}, n={len(h1_neg)}")
        print(f"   t({len(h1_pos)+len(h1_neg)-2})={t_stat:.3f}, p={p_val:.4f}")
        print(
            f"   Cohen's d={effect_size:.3f} ({'small' if abs(effect_size) < 0.5 else 'medium' if abs(effect_size) < 0.8 else 'large'} effect)")
        print(
            f"   Result: {'✓ SIGNIFICANT' if p_val < 0.05 else '✗ Not significant'}")

    # H2: Demographic bias
    h2_no = df[(df.prompt_family == "H2_demo") & (
        df.condition == "no_demo")]["vader_compound"]
    h2_yes = df[(df.prompt_family == "H2_demo") & (
        df.condition == "with_classyear")]["vader_compound"]

    if len(h2_no) > 1 and len(h2_yes) > 1:
        t_stat, p_val = stats.ttest_ind(h2_no, h2_yes)
        pooled_std = np.sqrt((h2_no.std()**2 + h2_yes.std()**2) / 2)
        effect_size = (h2_no.mean() - h2_yes.mean()) / \
            pooled_std if pooled_std > 0 else 0

        print(f"\n📊 H2: Demographic Bias (No Demo vs With Class Year)")
        print(
            f"   No demo: M={h2_no.mean():.3f}, SD={h2_no.std():.3f}, n={len(h2_no)}")
        print(
            f"   With demo: M={h2_yes.mean():.3f}, SD={h2_yes.std():.3f}, n={len(h2_yes)}")
        print(f"   t({len(h2_no)+len(h2_yes)-2})={t_stat:.3f}, p={p_val:.4f}")
        print(f"   Cohen's d={effect_size:.3f}")
        print(
            f"   Result: {'✓ SIGNIFICANT' if p_val < 0.05 else '✗ Not significant'}")

    # H3: Priming effect
    h3_unprimed = df[(df.prompt_family == "H3_priming") & (
        df.condition == "unprimed")]["vader_compound"]
    h3_primed = df[(df.prompt_family == "H3_priming") & (
        df.condition == "primed")]["vader_compound"]

    if len(h3_unprimed) > 1 and len(h3_primed) > 1:
        t_stat, p_val = stats.ttest_ind(h3_unprimed, h3_primed)
        pooled_std = np.sqrt((h3_unprimed.std()**2 + h3_primed.std()**2) / 2)
        effect_size = (h3_unprimed.mean() - h3_primed.mean()) / \
            pooled_std if pooled_std > 0 else 0

        print(f"\n📊 H3: Priming Bias (Unprimed vs Primed)")
        print(
            f"   Unprimed: M={h3_unprimed.mean():.3f}, SD={h3_unprimed.std():.3f}, n={len(h3_unprimed)}")
        print(
            f"   Primed: M={h3_primed.mean():.3f}, SD={h3_primed.std():.3f}, n={len(h3_primed)}")
        print(
            f"   t({len(h3_unprimed)+len(h3_primed)-2})={t_stat:.3f}, p={p_val:.4f}")
        print(f"   Cohen's d={effect_size:.3f}")
        print(
            f"   Result: {'✓ SIGNIFICANT' if p_val < 0.05 else '✗ Not significant'}")

    print("\n" + "="*80)
    print("\n✓ Analysis complete")
    print("  Next: python src/validate_claims.py")


if __name__ == "__main__":
    main()
