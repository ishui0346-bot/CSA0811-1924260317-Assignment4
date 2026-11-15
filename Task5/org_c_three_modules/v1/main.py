"""Organisation (c): main.py ties reader, stats and report together.  Run: python main.py [folder]"""
import sys
from pathlib import Path
import reader, stats, report

DATA = Path(__file__).resolve().parents[2] / "data" / "month"

def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA
    records, damaged = reader.read_records(folder)
    counts = stats.count_attendance(records)
    report.below_75_report(counts)
    print(f"({len(records)} records read, {damaged} damaged lines skipped)")

if __name__ == "__main__":
    main()
