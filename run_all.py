"""Optional helper: runs every non-interactive program. Usage: python run_all.py"""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).parent
PLAN = [("Task1", ["bad_script.py", "diagnose.py", "mess_bill.py"]),
        ("Task2", ["attendance.py", "trace_small.py"]),
        ("Task3", ["errors_demo.py", "misuse_experiment.py"]),
        ("Task4", ["test_buggy.py", "test_fixed.py"]),
        ("Task5", ["count_changes.py", "compare_demo.py"]),
        ("Task5/org_a_one_script/v2", ["attendance_script.py"]),
        ("Task5/org_b_one_module/v2", ["main.py"]),
        ("Task5/org_c_three_modules/v2", ["main.py"]),
        ("Task5/org_d_package/v2", ["main.py"]),
        ("Task6", ["demo_all.py", "test_fest.py", "run_fest.py"])]
for folder, files in PLAN:
    for f in files:
        print(f"\n{'=' * 70}\n{folder}/{f}\n{'=' * 70}", flush=True)
        subprocess.run([sys.executable, f], cwd=ROOT / folder)
