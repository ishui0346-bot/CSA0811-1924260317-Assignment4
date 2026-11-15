"""Task 4.2 - evidence: run process() for three days and print the log (buggy version)."""
import os
import buggy_library as lib

if os.path.exists(lib.LOG): os.remove(lib.LOG)
for day, books in ((1, ["Python Basics", "Java Notes"]), (2, ["Data Structures"]), (3, ["Networks", "Maths I", "Physics"])):
    lib.process(day, books)
    print(f"after day {day}, log file contains: {open(lib.LOG).read()!r}")
print("\nFINAL LOG (buggy):")
print(open(lib.LOG).read() or "(empty)")
os.remove(lib.LOG)
