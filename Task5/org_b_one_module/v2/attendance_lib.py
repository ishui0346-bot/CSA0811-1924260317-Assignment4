"""Organisation (b): the functions live in ONE module, attendance_lib.py."""
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

def longest_absent_streaks(records):
    """records (in date order) -> {regno: longest run of consecutive recorded days marked A}"""
    current, longest = {}, {}
    for regno, date, status in records:
        if status == "A":
            current[regno] = current.get(regno, 0) + 1
            longest[regno] = max(longest.get(regno, 0), current[regno])
        else:
            current[regno] = 0
    return longest

def below_75_report(counts):
    """Print the students below 75 %."""
    print("REPORT 1 - students below 75 %")
    for regno in sorted(counts):
        present, total = counts[regno]
        if is_below(present, total):
            print(f"  {regno}  {present}/{total}  {present * 100 / total:.1f}%")

def absent_streak_report(streaks, days=3):
    """Print the students absent for `days` or more consecutive recorded days."""
    print(f"REPORT 2 - students absent {days} or more consecutive days")
    for regno in sorted(streaks):
        if streaks[regno] >= days:
            print(f"  {regno}  longest absence: {streaks[regno]} days in a row")
