"""Task 2.4 - trace of the processing for one small file with a damaged line (printed step by step)."""
from pathlib import Path
from attendance import parse_line, is_below

path = Path(__file__).parent / "data" / "small" / "attendance_2024-08-01.txt"
counts, seen, damaged = {}, set(), []
print("File content:")
for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
    print(f"  {i}: {line}")
print(f"\n{'line':>4} | {'text':<24} | {'action':<44} | counts after")
with open(path, encoding="utf-8") as f:
    for n, line in enumerate(f, 1):
        text = line.rstrip("\n")
        try:
            regno, d, s = parse_line(text)
            seen.add((regno, d))
            rec = counts.setdefault(regno, [0, 0]); rec[1] += 1
            if s == "P": rec[0] += 1
            action = f"valid: {regno} on {d} = {s}"
        except ValueError as e:
            damaged.append((n, text, str(e)))
            action = f"DAMAGED -> logged ({e})"
        print(f"{n:>4} | {text:<24} | {action:<44} | {counts}")
print("\nResult:")
for regno in sorted(counts):
    p, t = counts[regno]
    print(f"  {regno}: {p}/{t} = {p * 100 / t:.1f}%  below 75%: {is_below(p, t)}")
print("  damaged log:", damaged)
