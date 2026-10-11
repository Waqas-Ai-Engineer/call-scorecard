import argparse
import glob
import json
import os
import sys
from .scorer import score_file
from .report import text_report, html_report


def main(argv=None):
    p = argparse.ArgumentParser(prog="callscore", description="Score call transcripts for lead capture, booking and compliance.")
    p.add_argument("paths", nargs="+", help="transcript files or folders (.txt/.json)")
    p.add_argument("--format", choices=["text", "json", "html"], default="text")
    p.add_argument("--out", help="write report to file")
    p.add_argument("--min-score", type=int, default=0, help="exit 1 if any call scores below this")
    a = p.parse_args(argv)
    files = []
    for x in a.paths:
        files += sorted(glob.glob(os.path.join(x, "*.txt")) + glob.glob(os.path.join(x, "*.json"))) if os.path.isdir(x) else [x]
    if not files:
        print("no transcripts found", file=sys.stderr)
        return 2
    results = [score_file(f) for f in files]
    if a.format == "json":
        body = json.dumps([r.to_dict() for r in results], indent=2)
    elif a.format == "html":
        body = html_report(results)
    else:
        body = text_report(results)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"wrote {a.out}")
    else:
        print(body)
    return 1 if any(r.score < a.min_score for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
