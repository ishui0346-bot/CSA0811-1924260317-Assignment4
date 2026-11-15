# Task 4 – File and Exception Forensics (K4)

**Run (inside this folder):** `python test_buggy.py` (evidence of the defects) · `python test_fixed.py` (repaired program, failing write, crash proof)
Files: `buggy_library.py` (the defective program, defects marked in comments), `library_log.py` (repaired), `test_buggy.py`, `test_fixed.py`. Each test deletes the files it creates.

## 4.1 Locate the defects
| Symptom | Cause in `buggy_library.py` | Explanation |
|---|---|---|
| **Earlier days are lost** | `open(LOG, "w")` | mode `"w"` **truncates** (empties) the file every time it is opened; each call to `process()` starts with an empty file, so only the last day survives. Evidence: after day 2 the log holds only day 2, after day 3 only day 3 |
| **Books join together** | `f.write(book)` without a separator / `"\n"` | `write()` writes exactly the characters given – it does **not** add a newline or space (unlike `print`). Evidence: `'Day 1: Python BasicsJava Notes'`, `'Day 3: NetworksMaths IPhysics'` |
| **Crash without saving / what happens when `write()` fails** | no `with`, no `close()`, no `try` | `write()` only copies text into a memory **buffer**; it reaches the disk when the buffer is flushed or the file is closed. If `write()` raises (disk full, closed or read-only file – e.g. `UnsupportedOperation: not writable`) or the program dies before `close()`, the exception propagates, the file is left open and unflushed, and the day's text can be lost or half-written. Proof (`test_fixed.py`, process killed after `write` with `os._exit`): without `close/with` the file holds `''`; with a `with` block it holds `'Day 1: Python Basics'`. (In normal CPython runs the file is also closed when `f` goes out of scope at the end of the function, so data is often saved by luck – this is not guaranteed in other Pythons, nor in a crash or while an exception still holds the frame.) |
Also: no error handling at all – any `OSError` ends the program and nothing is recorded about the failure.

## 4.2 Construct evidence
`test_buggy.py` runs `process()` for three days and prints the file after each day:
```
after day 1, log file contains: 'Day 1: Python BasicsJava Notes'
after day 2, log file contains: 'Day 2: Data Structures'            <- day 1 gone
after day 3, log file contains: 'Day 3: NetworksMaths IPhysics'      <- days 1, 2 gone; books joined
FINAL LOG (buggy):  Day 3: NetworksMaths IPhysics
```

## 4.3 Repair (`library_log.py`)
```python
line = f"Day {day}: " + "; ".join(books) + "\n"          # separators and a newline
try:
    with open(log_name, "a", encoding="utf-8") as f:      # append mode, always closed/flushed
        f.write(line)
    return True
except OSError as e:                                      # failure is recorded, program continues
    with open(ERROR_LOG, "a", encoding="utf-8") as err:
        err.write(f"Day {day}: could not write to {log_name}: {type(e).__name__}: {e}\n")
    return False
```
Result of `test_fixed.py` for the same three days:
```
Day 1: Python Basics; Java Notes
Day 2: Data Structures
Day 3: Networks; Maths I; Physics
```
A failing write (`process(4, …, log_name='no_such_folder/log.txt')`) returns `False` and `library_errors.log` records: `Day 4: could not write to no_such_folder/log.txt: FileNotFoundError: …` – no crash, no silent loss. The `"; ".join(...)` also handles one book and an empty list (`"Day 5: "`).

## 4.4 Two rules to prevent recurrence
1. **Choose the file mode deliberately:** use `"a"` to add to an existing log and `"w"` only when you really mean to replace the whole file; and remember `write()` adds nothing – always write the newline (or separators) yourself.
2. **Open files only with a `with` statement and wrap the write in a `try/except OSError`** that records the error – so the file is always closed/flushed and a failing write is reported instead of being lost or crashing the program.
