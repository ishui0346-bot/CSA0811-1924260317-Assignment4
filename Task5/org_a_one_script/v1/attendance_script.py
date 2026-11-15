"""Organisation (a): everything in ONE script.  Run: python attendance_script.py [folder]"""
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data" / "month"
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

def count_attendance(records):
    """records -> {regno: [present, total]}"""
    counts = {}
    for regno, date, status in records:
        rec = counts.setdefault(regno, [0, 0])
        rec[1] += 1
        if status == "P":
            rec[0] += 1
    return counts

def is_below(present, total, limit=75):
    """Exact integer test: present/total < limit %"""
    return present * 100 < limit * total

def below_75_report(counts):
    """Print the students below 75 %."""
    print("REPORT 1 - students below 75 %")
    for regno in sorted(counts):
        present, total = counts[regno]
        if is_below(present, total):
            print(f"  {regno}  {present}/{total}  {present * 100 / total:.1f}%")

def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA
    records, damaged = read_records(folder)
    counts = count_attendance(records)
    below_75_report(counts)
    print(f"({len(records)} records read, {damaged} damaged lines skipped)")

if __name__ == "__main__":
    main()
