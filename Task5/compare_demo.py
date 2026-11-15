"""Task 5.3 - evidence for the comparison: import styles, naming conflicts, testing, size of what must be loaded.
Run: python compare_demo.py"""
import sys, subprocess, tempfile, os, shutil
from pathlib import Path

root = Path(__file__).parent
pkg_dir = root / "org_d_package" / "v2"
sys.path.insert(0, str(pkg_dir))

print("== 1. import attendance.stats  versus  from attendance import stats ==")
import attendance
print("after 'import attendance' alone, is 'stats' available?", hasattr(attendance, "stats"), "(the package's __init__.py imports nothing)")
import attendance.stats
print("after 'import attendance.stats':   attendance.stats.is_below(5, 8) ->", attendance.stats.is_below(5, 8), "  (full dotted name needed every time)")
from attendance import stats
print("after 'from attendance import stats':   stats.is_below(6, 8) ->", stats.is_below(6, 8), "  (short name 'stats')")
from attendance.stats import is_below
print("after 'from attendance.stats import is_below':   is_below(6, 8) ->", is_below(6, 8), "  (function name only, origin not visible)")
print("   names now in this script:", [n for n in ("attendance", "stats", "is_below") if n in globals()])
print("   attendance.stats is stats:", attendance.stats is stats, "(same module object; Python loads it once)")

print("\n== 2. Naming conflicts ==")
tmp = tempfile.mkdtemp()
Path(tmp, "statistics.py").write_text("print('   >>> my own statistics.py was imported instead of the standard library')\n")
r = subprocess.run([sys.executable, "-c", "import statistics"], cwd=tmp, capture_output=True, text=True)
print("flat module named like a standard module (statistics.py in the working folder):\n", r.stdout.strip())
shutil.rmtree(tmp, ignore_errors=True)
print("In organisation (c) the modules 'reader', 'stats', 'report' are TOP-LEVEL names: any other 'stats' or 'report' on the path may clash.")
print("In organisation (d) they are attendance.reader / attendance.stats / attendance.report: the only top-level name is 'attendance'.")
def is_below(*a): return "my own function"                  # a local function with the same name
from attendance.stats import is_below as pkg_is_below
print("'from ... import is_below' can be overwritten by your own function of that name: is_below(6,8) =", is_below(6, 8), "| package version still reachable as", pkg_is_below(6, 8))

print("\n== 3. Testing and reuse: what must be loaded to test ONE function? (lines of code) ==")
def lines(p): return len(Path(p).read_text().splitlines())
for label, files in (("(a) one script", ["org_a_one_script/v2/attendance_script.py"]),
                     ("(b) one module", ["org_b_one_module/v2/attendance_lib.py"]),
                     ("(c) three modules", ["org_c_three_modules/v2/stats.py"]),
                     ("(d) package", ["org_d_package/v2/attendance/stats.py"])):
    print(f"   {label:<18} to test is_below(): {sum(lines(root / f) for f in files):>3} lines ({files[0].split('/')[-1]})")
print("   test of the boundary (exactly 75 %):", "is_below(6, 8) =", stats.is_below(6, 8), "(6/8 = 75.0 % is NOT below 75), is_below(5, 8) =", stats.is_below(5, 8))
assert stats.is_below(6, 8) is False and stats.is_below(5, 8) is True

print("\n== 4. __name__ == '__main__' ==")
for path in ("org_a_one_script/v2", "org_d_package/v2"):
    script = "attendance_script" if "org_a" in path else "main"
    r = subprocess.run([sys.executable, "-c", f"import {script}; print('   imported {script}: nothing printed by the import itself; __name__ =', {script}.__name__)"],
                       cwd=root / path, capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
