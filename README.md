# CSA08-<RegisterNumber>-Assignment4 – Robust Data Processing with Files, Exceptions, Modules and Packages

| | |
|---|---|
| Name | `<your name>` |
| Register number | `<your register number>` |
| Python version | 3.12 |
| Libraries | none to install – standard library only (see `requirements.txt`) |
| GitHub link | `<paste your repository link here>` |

> Replace the `<...>` parts and rename the folder to `CSA08-<RegisterNumber>-Assignment4` before pushing.

## How to use
1. Open this folder in VS Code (File → Open Folder). 2. Open the terminal, `cd` into a task folder, run the commands below and screenshot each output. 3. Upload the screenshots into the matching folder on GitHub. 4. Commit one task at a time (`git add Task1`, `git commit -m "Task 1: mess bill script repaired"`) – the commit history is checked.
Each task folder has a `README.md` with the written answers (diagnoses, designs, pseudocode, flowcharts, traces, tables of evidence) next to the code and the **input data files**. Output files created by the programs (`output/`, logs) appear when you run them. Optional: `python run_all.py` runs everything (a few seconds).
**Note:** the assignment paper shows only a placeholder for the Task 1 script (`[Code snippet: ...]`), so `Task1/bad_script.py` is reconstructed from the description.

| Task | Topic | Run (inside the folder) | Main evidence |
|---|---|---|---|
| 1 | Poor script → repaired design | `python bad_script.py` · `python diagnose.py` · `python mess_bill.py` | 9 deficiencies shown; old total `nan`, correct Rs 5831.15, 5 rejected lines listed |
| 2 | Biometric attendance design | `python attendance.py` · `python trace_small.py` | 22 files, 12 students, 5 damaged lines, 3 students below 75 %; trace table |
| 3 | Exceptions | `python errors_demo.py` · `python misuse_experiment.py` | every failure and its exception; custom `InvalidRecord`; try/except/else/finally; `raise … from …`; hidden typo `(0, 0)` |
| 4 | File forensics | `python test_buggy.py` · `python test_fixed.py` | earlier days lost, books joined, crash without saving; repaired log |
| 5 | Four organisations | `python count_changes.py` · `python compare_demo.py` · `cd org_d_package/v2 && python main.py` (and a, b, c) | files changed: 1 / 2 / 3 / 3; import styles; naming conflict |
| 6 | Fest registration package | `python demo_all.py` · `python test_fest.py` · `python run_fest.py` | 6 scenarios without a crash; 47/47 checks |

## Short result note per task
1. The volunteer script printed `nan` and silently dropped or mis-added lines; the repaired version (with, line by line, specific exceptions, Decimal, rejected list) gives Rs 5831.15 and lists the 5 rejected lines.
2. Attendance designed with a dict of `[present, total]`, a set of seen `(regno, date)` and a damaged-line log; below-75 test done with exact integers.
3. Line-level `InvalidRecord` and file-level `AttendanceFileError`, full try statement, and proof that `except Exception: pass` hides a typo.
4. `"w"` erased earlier days, `write()` adds no newline, and no `with` risks losing buffered data; repaired with `"a"`, `"\n"`, `with` and an error log.
5. Adding the second report changed 1 / 2 / 3 / 3 files in organisations (a) / (b) / (c) / (d); the package keeps names separate and is easiest to test.
6. The `fest` package handled clean, duplicate, invalid e-mail, damaged and missing-file cases without crashing.
