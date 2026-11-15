# Task 2 – From Requirement to File-Processing Design: Biometric Attendance Files (K3)

**Run (inside this folder):** `python make_data.py` (only if you want to regenerate the data; it is already included) · `python attendance.py` · `python trace_small.py`
Files: `data/attendance/2024-08/attendance_YYYY-MM-DD.txt` (22 working days, 12 students, 5 damaged lines), `data/small/` (the file used for the trace), `attendance.py` (processor), `output/` (created by the run).

## 2.1 Model the data
**Input file format** – one text file per day, one record per line, comma separated, UTF-8:
`register_number,date,status` → `192311001,2024-08-01,P` (register number = 9 digits, date = `YYYY-MM-DD`, status = `P` present / `A` absent).
**Damaged line** = wrong number of fields, register number not 9 digits, date not a real date, status not P/A, empty line, or a second record for the same student and date.
**Data structures:**
| Purpose | Structure | Why |
|---|---|---|
| counts per student | `dict` regno → `[present, total]` | O(1) update per line; one entry per student |
| records already counted | `set` of `(regno, date)` tuples | O(1) duplicate test; tuples are hashable |
| damaged lines | `list` of `(file, line number, text, reason)` | order of discovery kept; written to the log |
| files of the month | `list` from `Path.glob`, sorted | processed in date order |
**Output files:**
| File | Format | Content |
|---|---|---|
| `attendance_summary.csv` | `regno,present,total,percent` + header | one row per student |
| `below_75.txt` | `regno  present/total  percent%` | students below 75 % |
| `damaged_lines.log` | `file:line: 'text' -> reason`, with a header per run | every damaged line |
Assumption: a student's percentage = present days ÷ days with a valid record for that student. Test for "below 75 %" is the exact integer test `present*100 < 75*total` (no float rounding).

## 2.2 File operations (modes, encoding, methods)
| Operation | Mode | Method | Why |
|---|---|---|---|
| read a daily file | `"r"` | **iteration** `for line in f` (with `enumerate`) | one line at a time = small memory; line numbers for the log. (`readline()` is the same one line at a time by hand; `read()` loads everything and is used only for tiny files such as the trace) |
| write summary and below-75 list | `"w"` | `write()` | rebuilt completely at every run, so an old report can never be mixed with a new one |
| write damaged-line log | `"a"` | `write()` | history across runs is kept; earlier entries are never overwritten |
Encoding: `encoding="utf-8"` stated explicitly everywhere (the default depends on the computer, e.g. Windows uses cp1252, and would misread or fail); the CSV is opened with `newline=""` so line endings are identical on every system. Every file is opened with `with`. Folder and file names use `pathlib.Path` (`/` joins paths, `glob("attendance_*.txt")` finds files, works on Windows and Linux).

## 2.3 Pseudocode – monthly processing
```
ALGORITHM ProcessMonth
START
INPUT month_folder
IF month_folder does not exist THEN
    OUTPUT "folder not found"
    END
ENDIF
SET counts TO empty dictionary
SET seen TO empty set
SET damaged TO empty list
SET files TO sorted list of attendance_*.txt files IN month_folder
FOR each path IN files
    OPEN path for reading as UTF-8
    FOR each line, with its line_number
        IF line is empty THEN
            ADD (file, line_number, "empty line") TO damaged
        ELSE
            SPLIT line on commas
            IF not exactly 3 fields OR regno not 9 digits OR date invalid OR status not P or A THEN
                ADD (file, line_number, text, reason) TO damaged
            ELSE IF (regno, date) IS IN seen THEN
                ADD (file, line_number, text, "duplicate") TO damaged
            ELSE
                ADD (regno, date) TO seen
                SET counts[regno].total TO counts[regno].total + 1
                IF status is P THEN
                    SET counts[regno].present TO counts[regno].present + 1
                ENDIF
            ENDIF
        ENDIF
    ENDFOR
    CLOSE path
ENDFOR
OPEN attendance_summary.csv for writing
FOR each regno IN sorted counts
    WRITE regno, present, total, percent
ENDFOR
FOR each regno IN sorted counts
    IF present * 100 < 75 * total THEN
        WRITE regno to below_75.txt
    ENDIF
ENDFOR
APPEND all damaged lines TO damaged_lines.log
OUTPUT summary
END
```
(In the program a file that cannot be opened/decoded is caught, logged and skipped so one bad file does not stop the month – details in Task 3.)

## 2.4 Trace (output of `trace_small.py`; small file with a damaged line 3)
| Line | Text | Action | counts after |
|---|---|---|---|
| 1 | `192311001,2024-08-01,P` | valid, present | `{001: [1,1]}` |
| 2 | `192311002,2024-08-01,A` | valid, absent | `{001: [1,1], 002: [0,1]}` |
| 3 | `192311003,2024-08-01` | **damaged** (2 fields) → logged | unchanged |
| 4 | `192311001,2024-08-02,P` | valid | `{001: [2,2], 002: [0,1]}` |
| 5 | `192311002,2024-08-02,P` | valid | `{001: [2,2], 002: [1,2]}` |
Result: 192311001 = 2/2 = 100 %; 192311002 = 1/2 = 50 % → **below 75 %**; damaged log: line 3. The student on the damaged line (003) never enters `counts`.

## Result on the full month (output of `attendance.py`)
22 files read, 12 students, 5 damaged lines (bad status `Z`, 2 fields, regno `abc`, date `2024-13-45`, empty line). Below 75 %: 192311003 (63.6 %), 192311007 (54.5 %), 192311011 (63.6 %).
