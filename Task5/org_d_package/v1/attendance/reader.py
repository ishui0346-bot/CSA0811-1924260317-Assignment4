"""Package module: reading files."""
from pathlib import Path

def read_records(folder):
    """Read every attendance_*.txt in folder (sorted by date). Returns (records, damaged_count);
    records = list of (regno, date, status). Damaged lines are counted and skipped."""
    records, damaged = [], 0
    for path in sorted(Path(folder).glob("attendance_*.txt")):
        with open(path, encoding="utf-8") as f:
            for line in f:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) == 3 and parts[0].isdigit() and parts[2] in ("P", "A"):
                    records.append((parts[0], parts[1], parts[2]))
                else:
                    damaged += 1
    return records, damaged
