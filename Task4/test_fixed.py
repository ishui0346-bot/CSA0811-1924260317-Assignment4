"""Task 4.2 / 4.3 - same three days with the repaired version, plus a failing write, plus the 'crash without saving' proof."""
import os, subprocess, sys
import library_log as lib

for name in (lib.LOG, lib.ERROR_LOG):
    if os.path.exists(name): os.remove(name)
for day, books in ((1, ["Python Basics", "Java Notes"]), (2, ["Data Structures"]), (3, ["Networks", "Maths I", "Physics"])):
    print(f"day {day} saved:", lib.process(day, books))
print("\nFINAL LOG (repaired):")
print(open(lib.LOG).read())

print("== A failing write is reported, not a crash ==")
print("process(4, ..., log_name='no_such_folder/log.txt') ->", lib.process(4, ["Chemistry"], log_name="no_such_folder/log.txt"))
print("library_errors.log:", open(lib.ERROR_LOG).read().strip())

print("\n== What 'crashed without saving' means (the defect 3 of the buggy version) ==")
code_bad = "import os; f = open('crash_demo.txt', 'w'); f.write('Day 1: Python Basics'); os._exit(1)"       # no close(), process dies
code_good = "import os\nwith open('crash_demo2.txt', 'w') as f:\n    f.write('Day 1: Python Basics')\nos._exit(1)"                # closed by 'with' before the crash
subprocess.run([sys.executable, "-c", code_bad]); subprocess.run([sys.executable, "-c", code_good])
print("without close/with, after the crash the file holds:", repr(open("crash_demo.txt").read()), "(buffered text lost)")
print("with 'with' block,   after the crash the file holds:", repr(open("crash_demo2.txt").read()))
print("\nwrite() on a file opened for reading fails with:", end=" ")
try:
    with open(lib.LOG, "r") as f: f.write("x")
except Exception as e:
    print(type(e).__name__ + ":", e)
for n in ("crash_demo.txt", "crash_demo2.txt", lib.LOG, lib.ERROR_LOG): os.remove(n)
