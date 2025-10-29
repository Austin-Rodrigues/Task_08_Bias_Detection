from pathlib import Path
import json
from utils import read_text, read_data_block, sha256_str

DATA_PATH = "data/players_anonymized.csv"
PROMPTS = [
    ("H1_framing","positive","prompts/H1_positive.txt"),
    ("H1_framing","negative","prompts/H1_negative.txt"),
    ("H2_demo","no_demo","prompts/H2_nodemographics.txt"),
    ("H2_demo","with_classyear","prompts/H2_with_classyear.txt"),
    ("H3_priming","primed","prompts/H3_primed.txt"),
    ("H3_priming","unprimed","prompts/H3_unprimed.txt"),
]

def build_suite():
    data_block = read_data_block(DATA_PATH)
    base = f"You are given the following season stats (anonymized).\n\n{data_block}\n\n"
    data_hash = sha256_str(data_block)
    suite = []
    for fam, cond, pfile in PROMPTS:
        t = read_text(pfile)
        prompt = base + t + "\n\nDo not infer beyond the given numbers. Quote exact figures you rely on."
        suite.append({
            "family": fam,
            "condition": cond,
            "prompt": prompt,
            "data_hash": data_hash
        })
    return suite

if __name__ == "__main__":
    Path("results").mkdir(exist_ok=True)
    suite = build_suite()
    Path("results/prompt_suite.json").write_text(json.dumps(suite, indent=2), encoding="utf-8")
    print("Wrote results/prompt_suite.json")
