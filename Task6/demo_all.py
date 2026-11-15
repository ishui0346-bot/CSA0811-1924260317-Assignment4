"""Stage 5 - demonstration: runs the five scenarios (+ the combined 'full' set) and shows the results and logs.
Run: python demo_all.py"""
from pathlib import Path
from fest.pipeline import run

base = Path(__file__).parent
scenarios = [("clean", "Clean files (no problems)"),
             ("duplicate", "Duplicate registrations"),
             ("bad_email", "Invalid e-mail addresses"),
             ("damaged", "Damaged lines"),
             ("missing_file", "Missing department file (EEE.txt absent)"),
             ("full", "Everything together")]
overview = []
for folder, title in scenarios:
    print("\n" + "#" * 70 + f"\n# {title}   (input: data/{folder})\n" + "#" * 70)
    result = run(base / "data" / folder, base / "output" / folder)
    print(result["summary"])
    for name, key in (("duplicates.log", "duplicates"), ("errors.log", "errors")):
        content = (base / "output" / folder / name).read_text(encoding="utf-8").rstrip()
        if len(result[key]):
            print(f"--- {name}"); print(content)
    print("--- registrations_clean.csv"); print((base / "output" / folder / "registrations_clean.csv").read_text(encoding="utf-8").rstrip())
    overview.append((title, len(result["clean"]), len(result["duplicates"]), sum(d["invalid"] for d in result["departments"]),
                     sum(1 for d in result["departments"] if d["status"] != "read")))

print("\n" + "=" * 70 + "\nOVERVIEW - the program finished every scenario without crashing\n" + "=" * 70)
print(f"{'Scenario':<44}{'accepted':>9}{'dupl.':>7}{'invalid':>8}{'files lost':>11}")
for t, a, d, i, m in overview:
    print(f"{t:<44}{a:>9}{d:>7}{i:>8}{m:>11}")
