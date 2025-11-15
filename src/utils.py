"""
utils.py
Helper functions for reading data and generating hashes.
"""

from pathlib import Path
import hashlib


def read_text(fp: str) -> str:
    """Read text file content"""
    return Path(fp).read_text(encoding="utf-8")


def read_data_block(csv_path: str) -> str:
    """
    Read CSV and format as a data block for prompts.
    Handles your CSV format with season column.
    """
    csv_text = Path(csv_path).read_text(encoding="utf-8").strip()
    lines = csv_text.splitlines()
    header = lines[0].split(",")
    rows = [r.split(",") for r in lines[1:]]

    # Format as a readable table block
    out = ["Player statistics table (Season 2024):"]
    for r in rows:
        rec = dict(zip(header, r))
        out.append(
            f"- Player {rec['player_id']}: "
            f"{rec['goals']} goals, "
            f"{rec['assists']} assists, "
            f"{rec['turnovers']} turnovers, "
            f"{rec['minutes']} minutes, "
            f"class_year={rec['class_year']}"
        )
    return "\n".join(out)


def sha256_str(s: str) -> str:
    """Generate SHA256 hash of string for data verification"""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
