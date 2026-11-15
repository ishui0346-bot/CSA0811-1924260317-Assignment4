"""Task 1 (repaired) - total of the mess bills.
Line format: register_number,name,amount        Run: python mess_bill.py [filename]"""
import sys
from decimal import Decimal, InvalidOperation

def total_bills(filename):
    """Read `filename` line by line. Returns (total as Decimal, number of accepted lines, rejected list).
    rejected is a list of (line_number, line_text, reason). Raises FileNotFoundError / PermissionError /
    UnicodeDecodeError to the caller - those are file-level problems, not line-level ones."""
    total = Decimal("0.00")
    accepted = 0
    rejected = []
    with open(filename, encoding="utf-8") as f:              # closed automatically, even after an error
        for line_no, line in enumerate(f, start=1):          # one line in memory at a time
            text = line.strip()
            if text == "":
                continue                                     # blank line (e.g. the last one) is not an error
            parts = text.split(",")
            if len(parts) != 3:
                rejected.append((line_no, text, f"expected 3 fields, found {len(parts)}"))
                continue
            try:
                amount = Decimal(parts[2].strip())           # exact money, no float drift
            except InvalidOperation:
                rejected.append((line_no, text, f"amount {parts[2].strip()!r} is not a number"))
                continue
            if not amount.is_finite() or amount < 0:
                rejected.append((line_no, text, f"amount {amount} is not a valid bill"))
                continue
            total += amount
            accepted += 1
    return total, accepted, rejected

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "mess_bills.txt"
    try:
        total, accepted, rejected = total_bills(filename)
    except FileNotFoundError:
        print(f"File not found: {filename}"); return 1
    except PermissionError:
        print(f"No permission to read: {filename}"); return 1
    except UnicodeDecodeError as e:
        print(f"{filename} is not valid UTF-8 text: {e}"); return 1
    print(f"Accepted lines : {accepted}")
    print(f"Total          : Rs {total}")
    print(f"Rejected lines : {len(rejected)}")
    for line_no, text, reason in rejected:
        print(f"   line {line_no}: {text!r} -> {reason}")
    if rejected:
        with open("rejected_lines.txt", "w", encoding="utf-8") as out:     # record for the office to correct
            for line_no, text, reason in rejected:
                out.write(f"{line_no}\t{text}\t{reason}\n")
        print("Rejected lines saved in rejected_lines.txt")
    return 0

if __name__ == "__main__":
    sys.exit(main())
