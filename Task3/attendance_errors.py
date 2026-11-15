"""Task 3 - error handling for the attendance processor.
Line-level problem  -> InvalidRecord (one damaged line; the file is still processed)
File-level problem  -> AttendanceFileError (the whole file cannot be used)"""
import datetime

class InvalidRecord(Exception):
    """A single attendance line is damaged. Carries the line number, the text and the reason."""
    def __init__(self, line_no, text, reason):
        super().__init__(f"line {line_no}: {reason}: {text!r}")
        self.line_no, self.text, self.reason = line_no, text, reason

class AttendanceFileError(Exception):
    """The file as a whole cannot be processed (missing, unreadable, wrong encoding, empty)."""

def parse_record(line, line_no):
    """Return (regno, date_text, status) or RAISE InvalidRecord (with the original error as __cause__)."""
    text = line.rstrip("\n")
    try:
        parts = text.split(",")
        regno = parts[0].strip()                     # IndexError if the line is empty/short (parts[2] below)
        date_text = parts[1].strip()
        status = parts[2].strip().upper()
        if len(parts) > 3:
            raise ValueError(f"{len(parts)} fields instead of 3")
        int(regno)                                   # ValueError if the register number is not numeric
        datetime.date.fromisoformat(date_text)       # ValueError if not a real YYYY-MM-DD date
        if status not in ("P", "A"):
            raise ValueError(f"status {status!r} is not P or A")
    except IndexError as e:
        raise InvalidRecord(line_no, text, "too few fields") from e          # 'from e' keeps the original cause
    except ValueError as e:
        raise InvalidRecord(line_no, text, str(e)) from e
    return regno, date_text, status

def read_attendance_file(path):
    """Read one daily file. Returns (records, damaged). Raises AttendanceFileError for file-level problems.
    Shows the complete try statement: try / except (specific) / else / finally."""
    records, damaged = [], []
    f = None
    try:
        f = open(path, encoding="utf-8")             # may raise FileNotFoundError / PermissionError
        for line_no, line in enumerate(f, start=1):  # may raise UnicodeDecodeError while reading
            try:
                records.append(parse_record(line, line_no))
            except InvalidRecord as bad:             # damaged LINE: remember it and carry on
                damaged.append(bad)
    except FileNotFoundError as e:
        raise AttendanceFileError(f"{path}: file or folder does not exist") from e
    except PermissionError as e:
        raise AttendanceFileError(f"{path}: permission denied") from e
    except UnicodeDecodeError as e:
        raise AttendanceFileError(f"{path}: not valid UTF-8 (byte {e.start}: {e.reason})") from e
    else:                                            # runs only when NO exception happened in the try block
        if not records and not damaged:
            raise AttendanceFileError(f"{path}: file is empty")
        return records, damaged
    finally:                                         # runs ALWAYS (success, return, exception)
        if f is not None:
            f.close()
