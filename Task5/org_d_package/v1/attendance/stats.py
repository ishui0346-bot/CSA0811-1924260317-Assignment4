"""Package module: counting and percentages."""

def count_attendance(records):
    """records -> {regno: [present, total]}"""
    counts = {}
    for regno, date, status in records:
        rec = counts.setdefault(regno, [0, 0])
        rec[1] += 1
        if status == "P":
            rec[0] += 1
    return counts

def is_below(present, total, limit=75):
    """Exact integer test: present/total < limit %"""
    return present * 100 < limit * total
