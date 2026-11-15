"""The processing flow: department files -> read -> validate -> remove duplicates -> write clean file + logs."""
from pathlib import Path
from .errors import InvalidRegistration, DepartmentFileError
from .reader import read_department
from .validator import validate_line, duplicate_key
from . import writer

DEPARTMENTS = ["CSE", "ECE", "MECH", "CIVIL", "EEE"]

def run(input_dir, output_dir, departments=DEPARTMENTS):
    """Process all department files. Never raises for bad data: every problem is logged and the run goes on.
    Returns a dict with the clean records, duplicates, errors and the status of every department file."""
    input_dir, output_dir = Path(input_dir), Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    clean, duplicates, errors, dept_status = [], [], [], []
    first_seen = {}                                   # (regno, event) -> "CSE.txt:3"  : O(1) duplicate test
    for dept in departments:
        status = {"name": dept, "status": "read", "lines": 0, "valid": 0, "duplicates": 0, "invalid": 0}
        file_name = f"{dept}.txt"
        try:
            lines = read_department(input_dir / file_name)           # file-level problems
        except DepartmentFileError as e:
            errors.append(f"{file_name}: FILE PROBLEM - {e}" + (f" (cause: {type(e.__cause__).__name__})" if e.__cause__ else ""))
            status["status"] = "MISSING" if isinstance(e.__cause__, FileNotFoundError) else "UNREADABLE"
            dept_status.append(status)
            continue                                                  # the other departments are still processed
        status["lines"] = len(lines)
        for line_no, text in lines:
            try:
                record = validate_line(text, line_no)                 # line-level problems
            except InvalidRegistration as bad:
                errors.append(f"{file_name}:{bad.line_no}: {bad.reason} | {bad.text!r}")
                status["invalid"] += 1
                continue
            key = duplicate_key(record)
            if key in first_seen:
                duplicates.append(f"{file_name}:{line_no}: duplicate of {first_seen[key]} | {record['regno']} {record['event']}")
                status["duplicates"] += 1
                continue
            first_seen[key] = f"{file_name}:{line_no}"
            record["department"] = dept
            clean.append(record)
            status["valid"] += 1
        dept_status.append(status)
    result = {"clean": clean, "duplicates": duplicates, "errors": errors, "departments": dept_status}
    writer.write_clean(clean, output_dir)
    writer.write_log(output_dir / "duplicates.log", "Duplicate registrations removed", duplicates)
    writer.write_log(output_dir / "errors.log", "Invalid lines and file problems", errors)
    result["summary"] = writer.write_summary(result, output_dir)
    return result
