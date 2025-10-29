import re, csv, json
from pathlib import Path

def load_truth(csv_path="data/players_anonymized.csv"):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def extract_numbers(text):
    # naive parser for patterns like A(45g,30a,15t)
    patt = re.compile(r"([A-F])\((\d+)g,(\d+)a,(\d+)t\)")
    return patt.findall(text)

def validate_record(truth, player_id, g, a, t):
    for row in truth:
        if row["player_id"] == player_id:
            return (int(row["goals"]) == int(g) and int(row["assists"]) == int(a) and int(row["turnovers"]) == int(t))
    return False

def main():
    truth = load_truth()
    path = Path("results/outputs.jsonl")
    if not path.exists():
        raise SystemExit("No results/outputs.jsonl found.")
    mismatches = []
    for line in path.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        nums = extract_numbers(r["response_text"])
        for pid, g, a, t in nums:
            ok = validate_record(truth, pid, g, a, t)
            if not ok:
                mismatches.append({"run_id": r["run_id"], "player_id": pid, "g": g, "a": a, "t": t})
    Path("analysis").mkdir(exist_ok=True)
    out = Path("analysis/claim_mismatches.json")
    out.write_text(json.dumps(mismatches, indent=2), encoding="utf-8")
    print(f"Wrote {out} with {len(mismatches)} mismatches")

if __name__ == "__main__":
    main()
