# Task 5 – The Same Utility Organised Four Ways (K5)

The utility: read the daily attendance files of a month, print **Report 1 – students below 75 %**; after the change also **Report 2 – students absent 3 or more consecutive days**.
**Run (inside the chosen folder; every `main` takes an optional folder argument):**
```
cd org_a_one_script/v2     && python attendance_script.py
cd org_b_one_module/v2     && python main.py
cd org_c_three_modules/v2  && python main.py
cd org_d_package/v2        && python main.py
python count_changes.py        # 5.2: files changed per organisation (from the real v1/v2 files)
python compare_demo.py         # 5.3: import styles, naming conflicts, testing, __main__
```
`v1` = the original requirement (Report 1 only); `v2` = Report 2 added. `data/month/` holds 8 daily files for 6 students (shared by all). All four give identical output:
```
REPORT 1 - students below 75 %        192311002 5/8 62.5% | 192311003 5/8 62.5% | 192311005 4/8 50.0%
REPORT 2 - absent 3+ consecutive days 192311002 (3 in a row) | 192311005 (4 in a row)
(48 records read, 0 damaged lines skipped)
```
(192311004 has exactly 6/8 = 75.0 %, which is *not* below 75 – the boundary is tested with exact integer arithmetic.) "Consecutive" means consecutive recorded days (files in date order).

## 5.1 The four organisations
| | Layout | `if __name__ == "__main__":` |
|---|---|---|
| (a) one script | `attendance_script.py` – reading, counting, reports and `main()` together | guards `main()` |
| (b) one module + main | `attendance_lib.py` (all functions) + `main.py` (`import attendance_lib`) | in `main.py` |
| (c) three modules, one folder | `reader.py`, `stats.py`, `report.py` + `main.py` (`import reader, stats, report`; `report.py` does `import stats`) | in `main.py` |
| (d) package | `attendance/__init__.py` (docstring only), `attendance/reader.py`, `stats.py`, `report.py` (`from . import stats`, a relative import) + `main.py` (`from attendance import reader, stats, report`) | in `main.py` |
The guard `if __name__ == "__main__":` makes `main()` run only when the file is run directly; importing the file (for a test or by another program) runs nothing (shown in `compare_demo.py` section 4).

## 5.2 Change the requirement – how many files changed (output of `count_changes.py`)
| Organisation | Files before | **Files changed** | Lines added | Files changed (names) |
|---|---|---|---|---|
| (a) one script | 1 | **1** | 19 | `attendance_script.py` |
| (b) one module | 2 | **2** | 19 | `attendance_lib.py`, `main.py` |
| (c) three modules | 4 | **3** | 19 | `stats.py`, `report.py`, `main.py` (`reader.py` untouched) |
| (d) package | 5 | **3** | 19 | `attendance/stats.py`, `attendance/report.py`, `main.py` (`reader.py` and `__init__.py` untouched) |
The same 19 lines of new logic are written in every case; only *where* they go differs. More files changed does not mean more work – it shows where the responsibilities lie: the streak counting went into `stats`, the printing into `report`, the call into `main`, and **reading the files (`reader`) was not touched**, so it could not be broken.

## 5.3 Comparison
| Criterion | (a) script | (b) one module | (c) three modules | (d) package |
|---|---|---|---|---|
| **Readability** | one file of 69 lines – easy at this size, becomes long as features grow | 56-line library + short main | each file does one job (reader 16, stats 26, report 17 lines in v2) | same as (c), plus a clear namespace and a package docstring |
| **Reuse** | copy-paste only | `import attendance_lib` from any script in the folder | import single modules | `from attendance import stats` anywhere the package is on the path (can later be installed) |
| **Testing** | to test `is_below` the whole 69-line script (with reading and printing code) is loaded | 56 lines | 26 lines (`stats.py`) – no files, no printing | 26 lines; can test each module separately |
| **Naming conflicts** | none (one file) | module name `attendance_lib` is top-level | `reader`, `stats`, `report` are **top-level** names – they can clash with other modules of those names (demo: a local `statistics.py` hides the standard library module) | only `attendance` is top-level; inner names are `attendance.stats` etc., so no clash with other `stats` modules |
| **Folder complexity** | smallest | small | 4 files | 5 files and a sub-folder |
**Recommendation:** (a) for a one-off 20-line script; (d) for a utility that will grow, be tested and reused (the college's attendance programs); (b)/(c) are the middle steps.

### `import attendance.stats` versus `from attendance import stats` (output of `compare_demo.py`)
- `import attendance` alone does **not** make `attendance.stats` available (the empty `__init__.py` imports nothing): `hasattr(attendance, "stats")` → `False`.
- `import attendance.stats` loads the submodule; you must write the **full dotted name** each time: `attendance.stats.is_below(5, 8)`. It keeps the origin visible and cannot clash with your own names.
- `from attendance import stats` binds the short name `stats` to the same module object (`attendance.stats is stats` → `True`); `stats.is_below(6, 8)`.
- `from attendance.stats import is_below` binds just the function name: shortest to write, but it can be silently overwritten by your own `is_below` (demonstrated) and hides where the function came from.
Python loads the module only once (`sys.modules`), whichever form is used.
