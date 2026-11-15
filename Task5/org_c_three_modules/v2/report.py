"""Organisation (c): printing reports."""
import stats

def below_75_report(counts):
    """Print the students below 75 %."""
    print("REPORT 1 - students below 75 %")
    for regno in sorted(counts):
        present, total = counts[regno]
        if stats.is_below(present, total):
            print(f"  {regno}  {present}/{total}  {present * 100 / total:.1f}%")

def absent_streak_report(streaks, days=3):
    """Print the students absent for `days` or more consecutive recorded days."""
    print(f"REPORT 2 - students absent {days} or more consecutive days")
    for regno in sorted(streaks):
        if streaks[regno] >= days:
            print(f"  {regno}  longest absence: {streaks[regno]} days in a row")
