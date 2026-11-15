# Task 1 – File-Processing Design Review: Diagnose and Repair a Poor Script (K4)

**Run (inside this folder):** `python bad_script.py` · `python diagnose.py` · `python mess_bill.py` · `python mess_bill.py missing.txt` (shows the clean error message)
Data: `mess_bills.txt` (line = `register number,name,amount`; it contains 5 bad lines and a blank last line on purpose).
*Note:* the assignment paper shows only a placeholder for the volunteer's code, so `bad_script.py` is **reconstructed from the description** (open → `f.read()` → `total = 0` → split on `\n` → try/except/pass → print).

## Task 1.1 – Deficiencies found (evidence from `diagnose.py`)
| # | Deficiency | Evidence / consequence |
|---|---|---|
| 1 | Hard-coded file name/path (`"mess_bills.txt"`, in real life `C:/Users/office/...`) | works on one computer only; the office cannot choose another month's file |
| 2 | File never closed (no `with`, no `close()`) | `python -X dev` prints `ResourceWarning: unclosed file`; on a crash the data buffers/handles stay open |
| 3 | Whole file read at once (`f.read()` then `split("\n")`) | 50,000 lines ≈ 5 MiB, 500,000 lines ≈ 54 MiB of RAM (see run), versus ~20 KiB line by line |
| 4 | Bare `except:` with `pass` | hides **every** problem: bad amounts, missing fields and even typos (`totl` demo: no error, total stays 0) |
| 5 | Amounts added as `float` rupees | `0.1 + 0.2 = 0.30000000000000004`; paise errors accumulate; `float("NaN")` is accepted and turned the whole total into `nan` |
| 6 | Repeated `total = total + …` instead of `+=`/a function | repeated code, no reuse, hard to test |
| 7 | Last empty line (`"a\nb\n".split("\n")` → `['a','b','']`) | the empty item is "handled" only by accident through the bare except |
| 8 | Rejected lines unrecorded | the script prints a number only; the office cannot tell which students were left out |
| 9 | Commas inside an amount (`"1,200.00"`) split into extra fields | the old script added `1.0` instead of rejecting the line (silently wrong) |
Printed total of the old script: `nan`. Correct total: Rs 5831.15 (6 accepted lines, 5 rejected).

## Task 1.2 – Repaired design (`mess_bill.py`)
- **`total_bills(filename)`** – a function with the filename as a **parameter**, returns `(total, accepted_count, rejected_list)`; nothing is printed inside, so it can be tested and reused.
- **`with open(filename, encoding="utf-8") as f`** – closed automatically, also when an exception occurs.
- **Line-by-line reading** (`for line_no, line in enumerate(f, 1)`) – only one line in memory.
- **Specific exceptions:** `InvalidOperation` for an amount that is not a number; `FileNotFoundError`, `PermissionError`, `UnicodeDecodeError` handled in `main()` with clear messages. No bare `except`.
- **Rejected lines list** with line number, text and reason, printed and saved in `rejected_lines.txt`.
- **Decimal** for exact paise, and checks `is_finite()` and `amount >= 0` (so `NaN` and `-50.00` are rejected); blank lines are skipped on purpose.
Result: `Accepted lines: 6`, `Total: Rs 5831.15`, 5 rejected lines with reasons (abc, 2 fields, `"1,200.00"` → 4 fields, −50.00, NaN).

## Task 1.3 – Why it is safer for a file of 50,000 lines
1. **Memory:** line-by-line keeps ~20 KiB in memory however long the file is; `read()` + `split` needs about 5 MiB at 50,000 lines (54 MiB at 500,000) and grows with the file.
2. **One bad line cannot spoil or hide the result:** each line is validated; bad lines are rejected *and listed*, so the office can correct line 3 of 50,000 instead of never knowing.
3. **Exact money:** Decimal adds 50,000 amounts without paise drift.
4. **Resources and errors:** the file is always closed; missing file / no permission / wrong encoding give a clear message instead of a crash or a silently wrong total.
5. **Reusable and testable:** a function with a parameter works for any month's file and can be called from a test.
