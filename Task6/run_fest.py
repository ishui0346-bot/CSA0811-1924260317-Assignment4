"""Command line: python run_fest.py [input_folder] [output_folder]
Defaults: data/full  ->  output/full       The program never crashes on bad data; problems go to the log files."""
import sys, traceback
from pathlib import Path
from fest.pipeline import run

def main():
    base = Path(__file__).parent
    inp = Path(sys.argv[1]) if len(sys.argv) > 1 else base / "data" / "full"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else base / "output" / "full"
    if not inp.is_dir():
        print(f"Input folder not found: {inp}"); return 1
    try:
        result = run(inp, out)
    except OSError as e:                          # e.g. output folder cannot be created / disk full
        print(f"Cannot write the output files ({type(e).__name__}: {e})"); return 2
    except Exception:                             # the ONLY broad catch: last line of defence, it LOGS the full traceback
        print("Unexpected error - details saved in fatal_error.log")
        Path("fatal_error.log").write_text(traceback.format_exc(), encoding="utf-8"); return 3
    print(result["summary"])
    print(f"Files written to {out}: registrations_clean.csv, duplicates.log, errors.log, summary.txt")
    return 0

if __name__ == "__main__":
    sys.exit(main())
