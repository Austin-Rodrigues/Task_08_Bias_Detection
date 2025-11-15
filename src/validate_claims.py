"""
validate_claims.py
Checks LLM statements against ground truth data.
Detects fabrications and statistical misrepresentations.
Outputs: analysis/claim_mismatches.json, analysis/validation_report.txt
"""

import re
import csv
import json
from pathlib import Path
from collections import defaultdict


def load_ground_truth(csv_path="data/players_anonymized.csv"):
    """Load the actual player statistics"""
    with open(csv_path, newline="", encoding="utf-8") as f:
        return {row['player_id']: row for row in csv.DictReader(f)}


def extract_stat_claims(text):
    """
    Extract statistical claims from LLM response.
    Patterns: "Player A: 45 goals", "A(45g,30a,15t)", "A has 45 goals"
    """
    claims = []

    # Pattern 1: Player A: 45 goals, 30 assists
    pattern1 = r'Player\s+([A-F]):\s*(\d+)\s*goals?,\s*(\d+)\s*assists?,\s*(\d+)\s*turnovers?'
    for match in re.finditer(pattern1, text, re.IGNORECASE):
        claims.append({
            'player': match.group(1),
            'goals': int(match.group(2)),
            'assists': int(match.group(3)),
            'turnovers': int(match.group(4)),
            'pattern': 'format1'
        })

    # Pattern 2: A(45g,30a,15t)
    pattern2 = r'([A-F])\((\d+)g,(\d+)a,(\d+)t\)'
    for match in re.finditer(pattern2, text):
        claims.append({
            'player': match.group(1),
            'goals': int(match.group(2)),
            'assists': int(match.group(3)),
            'turnovers': int(match.group(4)),
            'pattern': 'format2'
        })

    # Pattern 3: Player A has 45 goals
    pattern3 = r'Player\s+([A-F])\s+(?:has|scored|recorded)\s+(\d+)\s+goals?'
    for match in re.finditer(pattern3, text, re.IGNORECASE):
        claims.append({
            'player': match.group(1),
            'goals': int(match.group(2)),
            'pattern': 'partial_goals'
        })

    # Pattern 4: A has 30 assists
    pattern4 = r'Player\s+([A-F])\s+(?:has|made|recorded)\s+(\d+)\s+assists?'
    for match in re.finditer(pattern4, text, re.IGNORECASE):
        claims.append({
            'player': match.group(1),
            'assists': int(match.group(2)),
            'pattern': 'partial_assists'
        })

    # Pattern 5: A with 15 turnovers
    pattern5 = r'Player\s+([A-F])\s+(?:with|has|committed)\s+(\d+)\s+turnovers?'
    for match in re.finditer(pattern5, text, re.IGNORECASE):
        claims.append({
            'player': match.group(1),
            'turnovers': int(match.group(2)),
            'pattern': 'partial_turnovers'
        })

    return claims


def validate_claim(truth, claim):
    """Check if claim matches ground truth"""
    player_id = claim['player']
    if player_id not in truth:
        return False, f"Player {player_id} not in dataset"

    actual = truth[player_id]
    errors = []

    if 'goals' in claim:
        if int(actual['goals']) != claim['goals']:
            errors.append(
                f"Goals: claimed {claim['goals']}, actual {actual['goals']}")

    if 'assists' in claim:
        if int(actual['assists']) != claim['assists']:
            errors.append(
                f"Assists: claimed {claim['assists']}, actual {actual['assists']}")

    if 'turnovers' in claim:
        if int(actual['turnovers']) != claim['turnovers']:
            errors.append(
                f"Turnovers: claimed {claim['turnovers']}, actual {actual['turnovers']}")

    if errors:
        return False, "; ".join(errors)

    return True, "Correct"


def main():
    """Main validation routine"""
    results_path = Path("results/outputs.jsonl")
    if not results_path.exists():
        raise SystemExit("❌ No results/outputs.jsonl found.\n"
                         "   Run: python src/run_experiment.py --convert")

    print("Validating LLM claims against ground truth...\n")

    truth = load_ground_truth()

    # Track all mismatches and statistics
    all_mismatches = []
    stats_by_condition = defaultdict(lambda: {'total_claims': 0, 'errors': 0})

    for line in results_path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        text = record["response_text"]

        # Extract claims from this response
        claims = extract_stat_claims(text)

        condition_key = f"{record['prompt_family']}_{record['condition']}"
        stats_by_condition[condition_key]['total_claims'] += len(claims)

        # Validate each claim
        for claim in claims:
            is_valid, message = validate_claim(truth, claim)

            if not is_valid:
                mismatch = {
                    "run_id": record["run_id"],
                    "model": record["model"],
                    "prompt_family": record["prompt_family"],
                    "condition": record["condition"],
                    "player": claim['player'],
                    "claim": claim,
                    "error": message,
                    "pattern": claim.get('pattern', 'unknown')
                }
                all_mismatches.append(mismatch)
                stats_by_condition[condition_key]['errors'] += 1

    # Save mismatches
    Path("analysis").mkdir(exist_ok=True)
    mismatch_file = Path("analysis/claim_mismatches.json")
    mismatch_file.write_text(json.dumps(
        all_mismatches, indent=2), encoding="utf-8")

    # Generate validation report
    report_lines = []
    report_lines.append("="*80)
    report_lines.append("CLAIM VALIDATION REPORT")
    report_lines.append("="*80)
    report_lines.append("")

    total_claims = sum(s['total_claims'] for s in stats_by_condition.values())
    total_errors = sum(s['errors'] for s in stats_by_condition.values())

    report_lines.append(f"Total claims extracted: {total_claims}")
    report_lines.append(f"Total errors found: {total_errors}")
    report_lines.append(
        f"Accuracy rate: {100*(1-total_errors/total_claims) if total_claims > 0 else 100:.1f}%")
    report_lines.append("")

    report_lines.append("Breakdown by condition:")
    report_lines.append("-" * 80)

    for condition, stats in sorted(stats_by_condition.items()):
        claims = stats['total_claims']
        errors = stats['errors']
        accuracy = 100 * (1 - errors/claims) if claims > 0 else 100
        report_lines.append(
            f"{condition:40} | Claims: {claims:3} | Errors: {errors:3} | Accuracy: {accuracy:5.1f}%")

    report_lines.append("")
    report_lines.append("="*80)

    if all_mismatches:
        report_lines.append("DETAILED MISMATCHES")
        report_lines.append("="*80)
        report_lines.append("")

        for i, mm in enumerate(all_mismatches, 1):
            report_lines.append(
                f"{i}. Model: {mm['model']} | Condition: {mm['condition']}")
            report_lines.append(f"   Player: {mm['player']}")
            report_lines.append(f"   Claim: {mm['claim']}")
            report_lines.append(f"   Error: {mm['error']}")
            report_lines.append("")
    else:
        report_lines.append("✓ No mismatches found! All claims are accurate.")
        report_lines.append("")

    report_lines.append("="*80)

    # Write report
    report_file = Path("analysis/validation_report.txt")
    report_file.write_text("\n".join(report_lines), encoding="utf-8")

    # Print to console
    print("\n".join(report_lines))

    print(f"\n✓ Saved {mismatch_file}")
    print(f"✓ Saved {report_file}")

    if total_errors > 0:
        print(f"\n⚠️  Found {total_errors} fabricated/incorrect claims")
        print(f"   Fabrication rate: {100*total_errors/total_claims:.1f}%")
    else:
        print("\n✓ All claims validated successfully!")


if __name__ == "__main__":
    main()
