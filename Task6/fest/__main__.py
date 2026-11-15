"""python -m fest <input_folder> <output_folder>"""
import sys
from .pipeline import run
if __name__ == "__main__":
    print(run(sys.argv[1], sys.argv[2])["summary"])
