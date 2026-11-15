"""Organisation (d): main.py uses the package.  Run: python main.py [folder]"""
import sys
from pathlib import Path
from attendance import reader, stats, report

DATA = Path(__file__).resolve().parents[2] / "data" / "month"

def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA
    records, damaged = reader.read_records(folder)
    counts = stats.count_attendance(records)
    report.below_75_report(counts)
    report.absent_streak_report(stats.longest_absent_streaks(records))
    print(f"({len(records)} records read, {damaged} damaged lines skipped)")

if __name__ == "__main__":
    main()
