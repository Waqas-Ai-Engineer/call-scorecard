import html


def text_report(results):
    out = []
    for r in results:
        out.append(f"{r.file}: {r.score}/100 [{r.grade}] outcome={r.outcome}" + ("  URGENT" if r.urgent else ""))
        for n, p, m, _ in r.checks:
            out.append(f"   {'ok ' if p == m else '-- '}{n:<26}{p:>3}/{m}")
        for c in r.coaching:
            out.append(f"   tip: {c}")
        out.append("")
    if results:
        avg = sum(r.score for r in results) / len(results)
        booked = sum(r.outcome == "booked" for r in results)
        out.append(f"{len(results)} calls | avg {avg:.1f} | booked {booked}/{len(results)}")
    return "\n".join(out)


def html_report(results):
    rows = []
    for r in results:
        color = {"A": "#1a7f37", "B": "#4c9a2a", "C": "#b08800", "D": "#c2570c", "F": "#cf222e"}[r.grade]
        tips = "<br>".join(html.escape(c) for c in r.coaching) or "None - great call"
        rows.append(
            f"<tr><td>{html.escape(r.file)}</td><td style='color:{color};font-weight:700'>{r.score} ({r.grade})</td>"
            f"<td>{r.outcome}{' / URGENT' if r.urgent else ''}</td><td>{tips}</td></tr>")
    avg = sum(r.score for r in results) / len(results) if results else 0
    return ("<!doctype html><meta charset='utf-8'><title>Call Scorecard</title>"
            "<style>body{font:15px system-ui;margin:2rem;max-width:1000px}table{border-collapse:collapse;width:100%}"
            "td,th{border:1px solid #ddd;padding:8px;vertical-align:top;text-align:left}th{background:#f6f8fa}</style>"
            f"<h1>Call Scorecard</h1><p>{len(results)} calls &middot; average {avg:.1f}/100</p>"
            "<table><tr><th>Call</th><th>Score</th><th>Outcome</th><th>Coaching</th></tr>" + "".join(rows) + "</table>")
