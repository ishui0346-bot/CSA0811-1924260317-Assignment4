"""Task 1.1 - evidence for each deficiency of bad_script.py (run: python diagnose.py)."""
import subprocess, sys, tempfile, os
from decimal import Decimal

print("1. Output of bad_script.py on mess_bills.txt:")
out = subprocess.run([sys.executable, "bad_script.py"], capture_output=True, text=True).stdout.strip()
print("   total printed =", out)
from mess_bill import total_bills
total, accepted, rejected = total_bills("mess_bills.txt")
print("   correct total =", total, f"({accepted} accepted, {len(rejected)} rejected)")
print("   -> the old script silently added the wrong amounts: line 6 ('\"1,200.00\"') is split on the comma and 1 is added; the 'NaN' line made the whole float total nan, '-50.00' was added as a negative bill, and 'abc' / the 2-field line vanished without a trace.")

print("\n2. Float paise drift: 0.1 + 0.2 added as float =", 0.1 + 0.2, "| Decimal =", Decimal("0.1") + Decimal("0.2"))
print("   sum of the file's 0.10 and 0.20 as float:", float("0.10") + float("0.20"))

print("\n3. File never closed (ResourceWarning shows with python -X dev):")
r = subprocess.run([sys.executable, "-X", "dev", "-c", "f = open('mess_bills.txt'); data = f.read()"], capture_output=True, text=True)
print("  ", (r.stderr.strip().splitlines() or ["(no warning)"])[0])

print("\n4. The whole file is read into memory by f.read() - peak memory:")
import tracemalloc
path = os.path.join(tempfile.gettempdir(), "mess_big.txt")
for n_lines in (50_000, 500_000):
    with open(path, "w") as f:
        for i in range(n_lines):
            f.write(f"192{i:06d},Student {i},{i % 3000}.{i % 100:02d}\n")
    tracemalloc.start(); data = open(path).read(); lines = data.split("\n"); a = tracemalloc.get_traced_memory()[1]; tracemalloc.stop(); del data, lines
    tracemalloc.start()
    with open(path) as f:
        for line in f: pass
    b = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"   {n_lines:>7} lines: read() + split {a / 1024 / 1024:6.1f} MiB   line by line {b / 1024:6.1f} KiB")
os.remove(path)

print("\n5. Bare except + pass hides EVERY error, including typos:")
try:
    total = 0
    for line in ["1,Arun,100"]:
        try:
            total = totl + float(line.split(",")[2])        # typo 'totl'
        except:
            pass
    print("   typo in the loop -> no error shown, total stays", total)
except NameError as e:
    print("   NameError", e)

print("\n6. Empty last line: 'a\\nb\\n'.split('\\n') ->", "a\nb\n".split("\n"), "(the empty item is only skipped because of the bare except)")
print("7. Rejected lines are not recorded anywhere: the old script prints only a number; the repaired one lists", len(rejected), "lines with reasons.")
