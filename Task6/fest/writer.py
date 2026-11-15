"""Writing the output files (all rebuilt on every run: mode "w"; UTF-8)."""
from pathlib import Path

def write_clean(records, out_dir):
    """registrations_clean.csv : regno;name;email;event;department"""
    with open(Path(out_dir) / "registrations_clean.csv", "w", encoding="utf-8", newline="") as f:
        f.write("regno;name;email;event;department\n")
        for r in records:
            f.write(f"{r['regno']};{r['name']};{r['email']};{r['event']};{r['department']}\n")

def write_log(path, header, entries):
    """One log file: a header line and one line per entry."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(header + f" ({len(entries)})\n")
        for e in entries:
            f.write(e + "\n")

def write_summary(result, out_dir):
    lines = ["FEST REGISTRATION SUMMARY", "=" * 60,
             f"{'Department':<12}{'File status':<22}{'Lines':>6}{'Valid':>7}{'Dupl.':>7}{'Invalid':>9}"]
    for d in result["departments"]:
        lines.append(f"{d['name']:<12}{d['status']:<22}{d['lines']:>6}{d['valid']:>7}{d['duplicates']:>7}{d['invalid']:>9}")
    lines += ["-" * 60,
              f"Accepted registrations : {len(result['clean'])}",
              f"Duplicates removed     : {len(result['duplicates'])}",
              f"Invalid / damaged lines: {sum(d['invalid'] for d in result['departments'])}",
              f"Department files missing or unreadable: {sum(1 for d in result['departments'] if d['status'] != 'read')}",
              "", "Registrations per event:"]
    per_event = {}
    for r in result["clean"]:
        per_event[r["event"]] = per_event.get(r["event"], 0) + 1
    for event in sorted(per_event):
        lines.append(f"  {event:<14}{per_event[event]:>4}")
    text = "\n".join(lines) + "\n"
    with open(Path(out_dir) / "summary.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return text
