"""Creates the sample biometric files: data/attendance/2024-08/attendance_YYYY-MM-DD.txt (one per working day).
Seeded, so the files are the same every time. Run once: python make_data.py"""
import random, datetime
from pathlib import Path

rnd = random.Random(24)
folder = Path(__file__).parent / "data" / "attendance" / "2024-08"
folder.mkdir(parents=True, exist_ok=True)
students = [f"1923110{i:02d}" for i in range(1, 13)]
attend_prob = {s: 0.92 for s in students}
for s in ("192311003", "192311007", "192311011"):          # students who will end up below 75 %
    attend_prob[s] = 0.60
days = [d for d in (datetime.date(2024, 8, 1) + datetime.timedelta(days=i) for i in range(31)) if d.weekday() < 5]
damaged_at = {days[2]: "192311004,2024-08-05,Z", days[5]: "192311009,2024-08", days[9]: "abc,2024-08-14,P",
              days[12]: "192311002,2024-13-45,P", days[15]: ""}          # one damaged line on selected days
for d in days:
    lines = [f"{s},{d.isoformat()},{'P' if rnd.random() < attend_prob[s] else 'A'}" for s in students]
    if d in damaged_at:
        lines.insert(4, damaged_at[d])
    (folder / f"attendance_{d.isoformat()}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"{len(days)} files written to {folder}")
