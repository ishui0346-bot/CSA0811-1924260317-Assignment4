"""Organisation (c): counting and percentages."""

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

def longest_absent_streaks(records):
    """records (in date order) -> {regno: longest run of consecutive recorded days marked A}"""
    current, longest = {}, {}
    for regno, date, status in records:
        if status == "A":
            current[regno] = current.get(regno, 0) + 1
            longest[regno] = max(longest.get(regno, 0), current[regno])
        else:
            current[regno] = 0
    return longest
