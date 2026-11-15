"""Task 4.3 - repaired library log: append mode, newlines, with statement, error log."""
LOG = "returned_books.log"
ERROR_LOG = "library_errors.log"

def process(day, books, log_name=LOG):
    """Append one line per day:  'Day 2: Python Basics; Java Notes'. Returns True if saved, False if writing failed."""
    line = f"Day {day}: " + "; ".join(books) + "\n"          # books separated, line ends with newline
    try:
        with open(log_name, "a", encoding="utf-8") as f:      # "a": earlier days stay; 'with': closed (and flushed) always
            f.write(line)
        return True
    except OSError as e:                                      # disk full, read-only file, permission, folder missing ...
        try:
            with open(ERROR_LOG, "a", encoding="utf-8") as err:
                err.write(f"Day {day}: could not write to {log_name}: {type(e).__name__}: {e}\n")
        except OSError:
            pass                                              # even the error log failed: nothing more can be done safely
        return False
