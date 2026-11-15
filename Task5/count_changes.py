"""Task 5.2 - how many files changed when the second report (absent 3 consecutive days) was added?
Compares each organisation's v1 (original requirement) with v2 (second report added). Run: python count_changes.py"""
import difflib
from pathlib import Path

root = Path(__file__).parent
print(f"{'organisation':<24}{'files in v1':>12}{'files changed':>15}{'files added':>13}{'lines added':>13}{'lines removed':>15}   changed files")
for org in sorted(root.glob("org_*")):
    v1, v2 = org / "v1", org / "v2"
    names1 = {p.relative_to(v1) for p in v1.rglob("*.py")}
    names2 = {p.relative_to(v2) for p in v2.rglob("*.py")}
    changed, added_lines, removed_lines = [], 0, 0
    for n in sorted(names1 & names2):
        a = (v1 / n).read_text().splitlines(); b = (v2 / n).read_text().splitlines()
        if a != b:
            changed.append(str(n).replace("\\", "/"))
            for line in difflib.unified_diff(a, b, lineterm="", n=0):
                if line.startswith("+") and not line.startswith("+++"): added_lines += 1
                if line.startswith("-") and not line.startswith("---"): removed_lines += 1
    print(f"{org.name:<24}{len(names1):>12}{len(changed):>15}{len(names2 - names1):>13}{added_lines:>13}{removed_lines:>15}   {', '.join(changed)}")
