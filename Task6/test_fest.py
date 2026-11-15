"""Unit tests for the fest package (assert-based). Run: python test_fest.py"""
import shutil, tempfile
from pathlib import Path
from fest.validator import is_valid_email, validate_line, duplicate_key
from fest.errors import InvalidRegistration, DepartmentFileError
from fest.reader import read_department
from fest.pipeline import run

results = []
def check(name, condition):
    results.append((name, bool(condition)))
    assert condition, name

# ---- e-mail validation (string methods only) ----
for good in ("a@b.co", "arun.kumar@college.edu", "x_y+z@mail.example.com", "a-b@c-d.org", "name%tag@x.io"):
    check(f"valid email {good}", is_valid_email(good))
for bad in ("", "plain", "a@b", "a@@b.com", "@b.com", "a@", "a b@c.com", "a@b.c", "a@.b.com", "a@b..com", "a@b.com.", ".a@b.com", "a.@b.com", "a..b@c.com", "a@b.c0m", "a@b_c.com", "a@b.1234", "a!b@c.com"):
    check(f"invalid email {bad!r}", not is_valid_email(bad))

# ---- line validation and normalisation ----
r = validate_line("  192311001 ;  arun   KUMAR ; Arun.Kumar@College.EDU ; dance  ", 1)
check("normalised record", r == {"regno": "192311001", "name": "Arun Kumar", "email": "arun.kumar@college.edu", "event": "Dance"})
for text, why in (("", "empty"), ("   ", "blank"), ("1;2;3", "3 fields"), ("1;2;3;4;5", "5 fields"), ("12345678;A;a@b.com;Dance", "8 digits"),
                  ("19231100x;A;a@b.com;Dance", "letter in regno"), ("192311001;;a@b.com;Dance", "empty name"), ("192311001;A;a@b.com;", "empty event"),
                  ("192311001;A;nomail;Dance", "bad email")):
    try:
        validate_line(text, 7); check(f"rejects {why}", False)
    except InvalidRegistration as e:
        check(f"rejects {why}", e.line_no == 7 and e.reason)
check("duplicate key ignores case and spaces of the event",
      duplicate_key(validate_line("192311001;A;a@b.com;Dance", 1)) == duplicate_key(validate_line("192311001;A;a@b.com;  DANCE ", 2)))
check("same student, different event is NOT a duplicate",
      duplicate_key(validate_line("192311001;A;a@b.com;Dance", 1)) != duplicate_key(validate_line("192311001;A;a@b.com;Quiz", 2)))

# ---- file-level problems ----
tmp = Path(tempfile.mkdtemp(prefix="fest_"))
try:
    try:
        read_department(tmp / "CSE.txt"); check("missing file raises", False)
    except DepartmentFileError as e:
        check("missing file -> DepartmentFileError caused by FileNotFoundError", isinstance(e.__cause__, FileNotFoundError))
    (tmp / "ECE.txt").write_bytes("192312001;D\xe9;d@x.com;Dance\n".encode("latin-1"))
    try:
        read_department(tmp / "ECE.txt"); check("bad encoding raises", False)
    except DepartmentFileError as e:
        check("wrong encoding -> DepartmentFileError caused by UnicodeDecodeError", isinstance(e.__cause__, UnicodeDecodeError))
    (tmp / "MECH.txt").mkdir()
    try:
        read_department(tmp / "MECH.txt"); check("folder raises", False)
    except DepartmentFileError as e:
        check("a folder instead of a file -> DepartmentFileError", e.__cause__ is not None)

    # ---- the pipeline never crashes ----
    res = run(tmp, tmp / "out")
    check("pipeline survives: missing + wrong encoding + folder (no file readable)", len(res["clean"]) == 0 and all(d["status"] != "read" for d in res["departments"]))
    check("every file problem is logged", len(res["errors"]) == 5)
    empty = tmp / "empty_in"; empty.mkdir()
    check("empty input folder -> no crash, 5 files reported missing", sum(d["status"] == "MISSING" for d in run(empty, tmp / "out2")["departments"]) == 5)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---- the sample data scenarios give the expected counts ----
base = Path(__file__).parent / "data"
out = Path(tempfile.mkdtemp(prefix="fest_out_"))
try:
    expected = {"clean": (10, 0, 0, 0), "duplicate": (7, 2, 0, 0), "bad_email": (5, 0, 8, 0), "damaged": (6, 0, 7, 0), "missing_file": (8, 0, 0, 1), "full": (9, 2, 5, 1)}
    for name, exp in expected.items():
        res = run(base / name, out / name)
        got = (len(res["clean"]), len(res["duplicates"]), sum(d["invalid"] for d in res["departments"]), sum(d["status"] != "read" for d in res["departments"]))
        check(f"scenario {name}: accepted/duplicates/invalid/files-lost = {exp}", got == exp)
finally:
    shutil.rmtree(out, ignore_errors=True)

print(f"{sum(ok for _, ok in results)} / {len(results)} checks passed")
for name, ok in results[:6]: print("  PASS", name)
print("  ...")
