"""Task 3.1 / 3.2 / 3.3 - trigger every failure and show the exception that Python raises."""
import os, stat, sys, shutil, tempfile, traceback
from pathlib import Path
from attendance_errors import *

tmp = Path(tempfile.mkdtemp(prefix="att_"))
print("working folder:", tmp, "\n")

def show(title, fn):
    try:
        fn()
        print(f"{title:<34} -> no exception")
    except Exception as e:
        print(f"{title:<34} -> {type(e).__name__}: {e}")

print("== 3.1 Built-in exceptions raised by the failures ==")
show("missing FILE", lambda: open(tmp / "nope.txt"))
show("missing FOLDER", lambda: open(tmp / "no_folder" / "a.txt"))
show("missing folder (listing)", lambda: list(os.scandir(tmp / "no_folder")))

secret = tmp / "locked.txt"; secret.write_text("192311001,2024-08-01,P\n")
os.chmod(secret, 0)
def read_locked(): open(secret).read()
try:
    read_locked(); real_perm = False
except PermissionError as e:
    real_perm = True; print(f"{'permission denied (chmod 000)':<34} -> {type(e).__name__}: {e}")
os.chmod(secret, stat.S_IRUSR | stat.S_IWUSR)
if not real_perm:                                    # running as administrator/root, or Windows: chmod does not block reading
    try:
        open(tmp)                                    # opening a FOLDER as a file
    except OSError as e:
        print(f"{'open a folder as a file':<34} -> {type(e).__name__}: {e}   (PermissionError on Windows, IsADirectoryError on Linux/Mac)")
    def simulated(): raise PermissionError(13, "Permission denied (simulated)", str(secret))
    show("permission denied (simulated)", simulated)

(tmp / "bad_encoding.txt").write_bytes("192311001,2024-08-01,P\n192311002,2024-08-01,\xe9\n".encode("latin-1"))
show("wrong encoding (latin-1 as utf-8)", lambda: open(tmp / "bad_encoding.txt", encoding="utf-8").read())
(tmp / "empty.txt").write_text("")
show("empty file (read)", lambda: print("   read() returned", repr(open(tmp / "empty.txt").read()), "<- NO exception: we must check for emptiness ourselves"))
def unpack_two_into_three():
    regno, date_text, status = "192311001,2024-08-01".split(",")      # only 2 values for 3 names
show("damaged line: unpacking 2 into 3", unpack_two_into_three)
show("damaged line: ValueError int('19x')", lambda: int("19x"))
show("damaged line: ValueError date", lambda: __import__("datetime").date.fromisoformat("2024-13-45"))
show("damaged line: IndexError parts[2]", lambda: "192311001,2024-08-01".split(",")[2])

print("\n== 3.2 InvalidRecord: raised in parse_record, handled in read_attendance_file ==")
good = tmp / "mixed.txt"
good.write_text("192311001,2024-08-01,P\n192311002,2024-08-01\n19x311003,2024-08-01,A\n192311004,2024-13-45,P\n192311005,2024-08-01,Q\n192311006,2024-08-01,A\n")
records, damaged = read_attendance_file(good)
print("valid records:", len(records), "| damaged:", len(damaged))
for bad in damaged:
    print(f"   InvalidRecord(line {bad.line_no}): {bad.reason}   | original cause: {bad.__cause__!r}")

print("\n== 3.3 Complete try statement: file-level errors are converted with 'raise ... from ...' ==")
for name in ("nope.txt", "bad_encoding.txt", "empty.txt", "mixed.txt"):
    try:
        recs, dmg = read_attendance_file(tmp / name)
    except AttendanceFileError as e:
        print(f"{name:<18} AttendanceFileError: {e}\n{'':<18} original cause kept in __cause__: {e.__cause__!r}")
    else:
        print(f"{name:<18} OK: {len(recs)} records, {len(dmg)} damaged  (this print runs in the caller's 'else')")

print("\nTraceback of a chained exception (the original error stays visible):")
try:
    read_attendance_file(tmp / "bad_encoding.txt")
except AttendanceFileError:
    traceback.print_exc(limit=0, file=sys.stdout)

print("\n'finally' proof - the file is closed even when an exception is raised:")
import attendance_errors
opened = []
real_open = open
def tracking_open(*a, **k):
    f = real_open(*a, **k); opened.append(f); return f
attendance_errors.open = tracking_open
try:
    attendance_errors.read_attendance_file(tmp / "bad_encoding.txt")
except AttendanceFileError:
    pass
print("   file closed after exception:", all(f.closed for f in opened), f"({len(opened)} file object opened)")
del attendance_errors.open

shutil.rmtree(tmp, ignore_errors=True)
print('\n(temporary folder removed)')
