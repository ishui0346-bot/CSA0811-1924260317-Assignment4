"""Custom exceptions of the fest package."""

class InvalidRegistration(Exception):
    """One registration line is damaged or has an invalid value (line-level problem)."""
    def __init__(self, line_no, text, reason):
        super().__init__(f"line {line_no}: {reason}")
        self.line_no, self.text, self.reason = line_no, text, reason

class DepartmentFileError(Exception):
    """A whole department file cannot be used: missing, unreadable, wrong encoding (file-level problem)."""
