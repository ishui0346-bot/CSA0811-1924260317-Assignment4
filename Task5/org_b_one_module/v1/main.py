"""Organisation (b): main script that imports the module.  Run: python main.py [folder]"""
import sys
from pathlib import Path
import attendance_lib

DATA = Path(__file__).resolve().parents[2] / "data" / "month"

def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else DATA
    records, damaged = attendance_lib.read_records(folder)
    counts = attendance_lib.count_attendance(records)
    attendance_lib.below_75_report(counts)
    print(f"({len(records)} records read, {damaged} damaged lines skipped)")

if __name__ == "__main__":
    main()
