"""Task 4 - the library program as written (with its defects). Each defect is marked."""
LOG = "returned_books.log"

def process(day, books):
    """Adds the returned books of one day to the log."""
    f = open(LOG, "w")                      # DEFECT 1: mode "w" erases the file every day -> earlier days lost
    f.write(f"Day {day}: ")                 # DEFECT 2: no newline after anything ...
    for book in books:
        f.write(book)                       # ... and none between books -> 'Python BasicsJava Notes' joins together
    # DEFECT 3: no close() and no 'with' -> if anything fails here the buffered text may never reach the disk
