"""Task 2 - monthly attendance processor (designed in README.md, pseudocode in section 2.3).
Input line:  register_number,date,status      e.g. 192311001,2024-08-01,P
Run:  python attendance.py [folder]            (default folder: data/attendance/2024-08)"""
import sys, datetime
from pathlib import Path

PRESENT, ABSENT = "P", "A"
THRESHOLD = 75                      # percent

def parse_line(line):
    """Return (regno, date_text, status) or raise ValueError('reason') for a damaged line."""
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 3:
        raise ValueError(f"expected 3 fields, found {len(parts)}")
    regno, date_text, status = parts
    if not (len(regno) == 9 and regno.isdigit()):
        raise ValueError(f"register number {regno!r} must be 9 digits")
    try:
        datetime.date.fromisoformat(date_text)
    except ValueError:
        raise ValueError(f"date {date_text!r} is not YYYY-MM-DD")
    status = status.upper()
    if status not in (PRESENT, ABSENT):
        raise ValueError(f"status {status!r} must be P or A")
    return regno, date_text, status

def process_file(path, counts, seen, damaged):
    """Add the records of one daily file to counts = {regno: [present, total]}.
    seen = set of (regno, date) already counted; damaged = list of (filename, line_no, text, reason)."""
    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            text = line.rstrip("\n")
            if text.strip() == "":
                damaged.append((path.name, line_no, "", "empty line")); continue
            try:
                regno, date_text, status = parse_line(text)
            except ValueError as e:
                damaged.append((path.name, line_no, text, str(e))); continue
            if (regno, date_text) in seen:
                damaged.append((path.name, line_no, text, "duplicate record for this student and date")); continue
            seen.add((regno, date_text))
            rec = counts.setdefault(regno, [0, 0])
            rec[1] += 1
            if status == PRESENT:
                rec[0] += 1

def process_month(folder):
    """Process every attendance_*.txt in folder (sorted by name). Returns (counts, damaged, files_read, files_failed)."""
    folder = Path(folder)
    counts, seen, damaged, failed = {}, set(), [], []
    files = sorted(folder.glob("attendance_*.txt"))
    for path in files:
        try:
            process_file(path, counts, seen, damaged)
        except (OSError, UnicodeDecodeError) as e:           # file-level problems: log and go on with the next file
            failed.append((path.name, f"{type(e).__name__}: {e}"))
    return counts, damaged, files, failed

def is_below(present, total):
    """Exact integer test for present/total < 75 %  (no float rounding)."""
    return present * 100 < THRESHOLD * total

def write_outputs(counts, damaged, out_dir, run_label):
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "attendance_summary.csv", "w", encoding="utf-8", newline="") as f:      # "w": rebuilt on every run
        f.write("regno,present,total,percent\n")
        for regno in sorted(counts):
            p, t = counts[regno]
            f.write(f"{regno},{p},{t},{p * 100 / t:.1f}\n")
    with open(out_dir / "below_75.txt", "w", encoding="utf-8") as f:
        for regno in sorted(counts):
            p, t = counts[regno]
            if is_below(p, t):
                f.write(f"{regno}  {p}/{t}  {p * 100 / t:.1f}%\n")
    with open(out_dir / "damaged_lines.log", "a", encoding="utf-8") as f:                       # "a": history is kept
        f.write(f"--- run {run_label}: {len(damaged)} damaged line(s) ---\n")
        for name, line_no, text, reason in damaged:
            f.write(f"{name}:{line_no}: {text!r} -> {reason}\n")

def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "data" / "attendance" / "2024-08"
    if not folder.is_dir():
        print(f"Folder not found: {folder}"); return 1
    counts, damaged, files, failed = process_month(folder)
    if not files:
        print(f"No attendance files in {folder}"); return 1
    out_dir = Path(__file__).parent / "output"
    write_outputs(counts, damaged, out_dir, folder.name)
    print(f"Files read: {len(files) - len(failed)} of {len(files)} | students: {len(counts)} | damaged lines: {len(damaged)}")
    for name, why in failed: print("  FAILED", name, why)
    print(f"{'regno':<11}{'present':>8}{'total':>7}{'percent':>9}")
    for regno in sorted(counts):
        p, t = counts[regno]
        flag = "  < 75%" if is_below(p, t) else ""
        print(f"{regno:<11}{p:>8}{t:>7}{p * 100 / t:>8.1f}%{flag}")
    print("Damaged lines:")
    for name, line_no, text, reason in damaged: print(f"  {name}:{line_no}: {text!r} -> {reason}")
    print(f"Outputs written to {out_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
