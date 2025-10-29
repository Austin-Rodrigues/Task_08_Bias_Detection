from pathlib import Path
import hashlib

def read_text(fp: str) -> str:
    return Path(fp).read_text(encoding="utf-8")

def read_data_block(csv_path: str) -> str:
    csv_text = Path(csv_path).read_text(encoding="utf-8").strip()
    lines = csv_text.splitlines()
    header = lines[0].split(",")
    rows = [r.split(",") for r in lines[1:]]
    # Format as a simple table block for prompts
    out = ["Player statistics table:"]
    for r in rows:
        rec = dict(zip(header, r))
        out.append(f"- Player {rec['player_id']}: {rec['goals']} goals, {rec['assists']} assists, "
                   f"{rec['turnovers']} turnovers, {rec['minutes']} minutes, class_year={rec['class_year']}")
    return "\n".join(out)

def sha256_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
