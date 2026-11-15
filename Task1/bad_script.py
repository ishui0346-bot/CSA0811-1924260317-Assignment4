"""Task 1 - the volunteer's script, reconstructed from the description in the assignment
(the paper shows only '[Code snippet: ...]'; this version contains every defect that the task lists)."""
f = open("mess_bills.txt")          # hard-coded name/path, never closed
data = f.read()                     # whole file in memory at once
total = 0
for line in data.split("\n"):       # the last empty line also becomes an item
    try:
        parts = line.split(",")
        total = total + float(parts[2])      # float rupees, repeated +
    except:                         # bare except + pass: every problem silently ignored
        pass
print(total)
