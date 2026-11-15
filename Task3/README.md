# Task 3 – Design the Error Handling: Exceptions in the Attendance Processor (K4)

**Run (inside this folder):** `python errors_demo.py` · `python misuse_experiment.py`  (module: `attendance_errors.py`)
`errors_demo.py` creates its test files in a temporary folder and deletes it at the end.

## 3.1 Identify the failures (output of `errors_demo.py`)
| Failure | What really happens | Exception raised | Level |
|---|---|---|---|
| Month folder missing | `os.scandir`/`Path.glob` on a folder that does not exist | `FileNotFoundError` (for `glob` an empty result – so check `folder.is_dir()` first) | file-level |
| Daily file missing | `open("nope.txt")` | `FileNotFoundError: [Errno 2] No such file or directory` | file-level |
| Permission denied | reading a file with no read right (`chmod 000`); on Windows also opening a folder as a file | `PermissionError: [Errno 13]`; (opening a folder on Linux gives `IsADirectoryError`) | file-level |
| Wrong encoding | a latin-1 file (byte `0xe9`) read as UTF-8 | `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 …` – raised **while reading**, not at `open()` | file-level |
| Damaged line – wrong number of values | `regno, d, s = "a,b".split(",")` | `ValueError: not enough values to unpack (expected 3, got 2)` | line-level |
| Damaged line – short line indexed | `parts[2]` on a 2-field line | `IndexError: list index out of range` | line-level |
| Damaged line – bad number / date / status | `int("19x311003")`, `date.fromisoformat("2024-13-45")` | `ValueError` (`invalid literal for int()`, `month must be in 1..12`) | line-level |
| Empty file | `read()` returns `''` | **no exception at all** – the program must check for it itself | file-level |
Note: if the demo is run with administrator/root rights or on Windows, `chmod 000` does not stop reading; the demo then shows the "open a folder as a file" error and a clearly-labelled **simulated** `PermissionError` (the exception is real, only the trigger is simulated).
Design rule: **line-level problems** must not stop the file; **file-level problems** make the whole file unusable but must not stop the month.

## 3.2 Custom exception `InvalidRecord`
```python
class InvalidRecord(Exception):
    def __init__(self, line_no, text, reason): ...      # carries line number, text, reason
```
- **Raised in** `parse_record(line, line_no)` whenever a line is damaged – the low-level `IndexError`/`ValueError` is translated into one meaningful exception: `raise InvalidRecord(...) from e`.
- **Handled in** `read_attendance_file` inside the line loop: `except InvalidRecord as bad: damaged.append(bad)` – the line is remembered for the log and the loop goes on with the next line.
- Why a custom exception: callers catch one clear type (`InvalidRecord`) instead of guessing `(ValueError, IndexError, TypeError)`; the reason travels with it; and a real bug (e.g. `NameError`) is **not** mistaken for a damaged line. A second class `AttendanceFileError` represents file-level problems.
Output: `InvalidRecord(line 2): too few fields | original cause: IndexError('list index out of range')` – the four damaged lines of the test file are reported, the two good ones are kept.

## 3.3 The complete try statement (`read_attendance_file`)
```python
try:
    f = open(path, encoding="utf-8")           # may raise FileNotFoundError / PermissionError
    for ... : records.append(parse_record(...)) # may raise UnicodeDecodeError while reading
except FileNotFoundError as e:   raise AttendanceFileError("... does not exist") from e
except PermissionError as e:     raise AttendanceFileError("... permission denied") from e
except UnicodeDecodeError as e:  raise AttendanceFileError("... not valid UTF-8") from e
else:                            # only if NOTHING went wrong in the try block
    if not records and not damaged: raise AttendanceFileError("file is empty")
    return records, damaged
finally:                         # ALWAYS
    if f is not None: f.close()
```
- **try** – the code that may fail. **except (specific)** – each failure gets its own handler and message; no broad catch. **else** – code that should run only on success (the "empty file" check; keeping it out of `try` prevents it from being caught by accident). **finally** – clean-up that must happen whatever occurs (closing the file; the demo proves `closed == True` after an exception).
- **`raise … from e`** sets `__cause__`: the output shows `original cause kept in __cause__: FileNotFoundError(2, 'No such file or directory')`, and a printed traceback shows *"The above exception was the direct cause of the following exception"* – the low-level error is not lost when it is converted into `AttendanceFileError`.
- (`with open(...)` is the normal way to close files and is used in the other tasks; the explicit `finally` here is to show the full statement.)

## 3.4 Misuse experiment (output of `misuse_experiment.py`)
The same counting function, file with 2 present, 1 damaged line (line 3):
| Version | Result |
|---|---|
| correct code, `except InvalidRecord` | `(2, 1)` – correct |
| typo `presnt += 1` + `except InvalidRecord` | **crashes immediately**: `UnboundLocalError: cannot access local variable 'presnt' …` – the typo is found at once |
| typo `presnt += 1` + `except Exception: pass` | `(0, 0)` – **no error, silently wrong** (0 present and the damaged line is not counted either) |
**Why the error is hidden:** `except Exception` catches *almost every* error, including the `UnboundLocalError` produced by the typo (and `NameError`, `TypeError`, …), and `pass` throws it away. Every line therefore "fails" quietly, so the totals are zero and nothing in the output points to the cause. Rules: catch **specific** exceptions you can really handle; never `pass` silently – at least log; let unexpected errors (bugs) reach the surface.
