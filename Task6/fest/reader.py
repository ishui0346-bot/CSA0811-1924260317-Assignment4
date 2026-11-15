"""Reading one department file."""
from pathlib import Path
from .errors import DepartmentFileError

def read_department(path):
    """Return the lines of a department file as a list of (line_number, text).
    Raises DepartmentFileError (with the original error as __cause__) for file-level problems."""
    path = Path(path)
    lines = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                lines.append((line_no, line.rstrip("\n")))
    except FileNotFoundError as e:
        raise DepartmentFileError(f"{path.name}: file not found") from e
    except PermissionError as e:
        raise DepartmentFileError(f"{path.name}: permission denied") from e
    except IsADirectoryError as e:
        raise DepartmentFileError(f"{path.name}: is a folder, not a file") from e
    except UnicodeDecodeError as e:
        raise DepartmentFileError(f"{path.name}: not valid UTF-8 text (byte {e.start})") from e
    return lines
