"""Package fest - College Fest Registration Desk.
errors    : custom exceptions
reader    : reads one department file (file-level errors -> DepartmentFileError)
validator : validates one line (string methods only, no regular expressions)
writer    : writes the clean file, the logs and the summary
pipeline  : ties the steps together and never lets one bad line or file stop the run"""
