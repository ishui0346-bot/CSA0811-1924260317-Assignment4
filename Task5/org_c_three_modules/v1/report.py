"""Organisation (c): printing reports."""
import stats

def below_75_report(counts):
    """Print the students below 75 %."""
    print("REPORT 1 - students below 75 %")
    for regno in sorted(counts):
        present, total = counts[regno]
        if stats.is_below(present, total):
            print(f"  {regno}  {present}/{total}  {present * 100 / total:.1f}%")
