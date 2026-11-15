"""Task 3.4 - Misuse experiment: a broad 'except Exception: pass' hides a typo.
The same function is run in three versions on the same file. Run: python misuse_experiment.py"""
import tempfile, os
from attendance_errors import parse_record, InvalidRecord

DATA = "192311001,2024-08-01,P\n192311002,2024-08-01,A\n192311003,2024-08-01\n192311004,2024-08-01,P\n"
path = os.path.join(tempfile.gettempdir(), "misuse_demo.txt")
with open(path, "w") as f:
    f.write(DATA)

def count_present_correct(path):
    """Specific exception, no typo."""
    present, damaged = 0, 0
    with open(path) as f:
        for n, line in enumerate(f, 1):
            try:
                regno, d, s = parse_record(line, n)
                if s == "P":
                    present += 1
            except InvalidRecord:
                damaged += 1
    return present, damaged

def count_present_typo_specific(path):
    """Typo introduced ('presnt'), but the except is SPECIFIC -> the typo is not caught."""
    present, damaged = 0, 0
    with open(path) as f:
        for n, line in enumerate(f, 1):
            try:
                regno, d, s = parse_record(line, n)
                if s == "P":
                    presnt += 1                      # TYPO: should be present += 1
            except InvalidRecord:
                damaged += 1
    return present, damaged

def count_present_typo_hidden(path):
    """Same typo, but with a broad 'except Exception: pass' -> the typo is swallowed."""
    present, damaged = 0, 0
    with open(path) as f:
        for n, line in enumerate(f, 1):
            try:
                regno, d, s = parse_record(line, n)
                if s == "P":
                    presnt += 1                      # TYPO: UnboundLocalError ... swallowed below
            except Exception:
                pass

    return present, damaged

print("expected for this file: 2 present, 1 damaged (line 3)\n")
print("1. correct code, specific except      ->", count_present_correct(path))
print("2. typo + specific except InvalidRecord ->", end=" ")
try:
    print(count_present_typo_specific(path))
except UnboundLocalError as e:
    print(f"CRASH with a clear message: UnboundLocalError: {e}   <- the bug is found immediately")
print("3. typo + 'except Exception: pass'     ->", count_present_typo_hidden(path), "  <- NO error, result silently WRONG (0 present, 0 damaged, instead of 2 and 1)")
os.remove(path)
