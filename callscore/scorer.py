"""Transcript parsing + scoring."""
import json
import os
import re
from dataclasses import dataclass, field, asdict
from . import rules as R

LINE = re.compile(r"^\s*(agent|ai|assistant|receptionist|caller|customer|client|patient|user)\s*[:\-]\s*(.+)$", re.I)
AGENT_ROLES = {"agent", "ai", "assistant", "receptionist"}


@dataclass
class Turn:
    role: str  # "agent" | "caller"
    text: str


@dataclass
class Result:
    file: str
    score: int = 0
    grade: str = "F"
    outcome: str = "no_booking"
    urgent: bool = False
    captured: dict = field(default_factory=dict)
    checks: list = field(default_factory=list)  # (name, points, max, note)
    coaching: list = field(default_factory=list)

    def to_dict(self):
        d = asdict(self)
        d["checks"] = [dict(name=n, points=p, max=m, note=t) for n, p, m, t in self.checks]
        return d


def parse(text):
    """Accept 'Role: text' lines or a JSON list of {role,text}."""
    text = text.strip()
    turns = []
    if text.startswith("["):
        for t in json.loads(text):
            role = "agent" if str(t.get("role", "")).lower() in AGENT_ROLES else "caller"
            turns.append(Turn(role, str(t.get("text", ""))))
        return turns
    for ln in text.splitlines():
        m = LINE.match(ln)
        if m:
            role = "agent" if m.group(1).lower() in AGENT_ROLES else "caller"
            turns.append(Turn(role, m.group(2).strip()))
        elif turns and ln.strip():
            turns[-1].text += " " + ln.strip()
    return turns


def _join(turns, role=None):
    return " ".join(t.text for t in turns if role is None or t.role == role)


def score(turns, file="<stdin>"):
    r = Result(file=file)
    agent, caller, allt = _join(turns, "agent"), _join(turns, "caller"), _join(turns)
    first_agent = next((t.text for t in turns if t.role == "agent"), "")

    def add(name, pts, mx, note):
        r.checks.append((name, pts, mx, note))

    r.urgent = bool(R.EMERGENCY.search(caller))
    add("Greeting", 5 if R.GREETING.search(first_agent) else 0, 5, "Opens with a greeting/business name")
    add("Recording disclosure", 5 if R.RECORDING.search(agent) else 0, 5, "Mentions call recording (required in many regions)")

    cap = {
        "name": bool(R.NAME.search(allt)),
        "phone": bool(R.PHONE.search(caller)),
        "address": bool(R.ADDRESS.search(allt)),
        "email": bool(R.EMAIL.search(allt)),
    }
    r.captured = cap
    pts = 6 * cap["name"] + 10 * cap["phone"] + 8 * cap["address"] + 3 * cap["email"]
    add("Lead capture", pts, 27, "name 6, phone 10, address 8, email 3")

    add("Empathy", 8 if R.EMPATHY.search(agent) else 0, 8, "Acknowledges the caller's problem")

    booked = bool(R.BOOKED.search(agent)) and bool(R.TIME_OFFER.search(agent))
    offered = bool(R.TIME_OFFER.search(agent))
    r.outcome = "booked" if booked else ("handoff" if R.HANDOFF.search(agent) else "no_booking")
    add("Booking", 25 if booked else (10 if offered else 0), 25, "Confirmed slot = 25, offered times only = 10")

    if r.urgent:
        fast = bool(re.search(r"\b(today|tonight|right away|as soon as|asap|within the hour|emergency|dispatch)", agent, re.I))
        add("Urgency handling", 10 if fast else 0, 10, "Emergency caller gets same-day/dispatch response")
    else:
        add("Urgency handling", 10, 10, "No emergency detected (full marks)")

    if R.OBJECTION.search(caller) or R.PRICE.search(caller):
        add("Objection/price handling", 10 if R.HANDLED.search(agent) else 0, 10, "Offers free estimate/financing/warranty")
    else:
        add("Objection/price handling", 10, 10, "No objection raised (full marks)")

    add("Next step stated", 5 if R.NEXT_STEP.search(agent) else 0, 5, "Tells caller what happens next")
    bad = R.UNSAFE_PROMISE.search(agent)
    add("No risky promises", 0 if bad else 5, 5, "No guarantees of outcomes/exact prices")

    r.score = sum(p for _, p, _, _ in r.checks)
    r.grade = "A" if r.score >= 90 else "B" if r.score >= 75 else "C" if r.score >= 60 else "D" if r.score >= 40 else "F"
    tips = {
        "Greeting": "Open with a greeting and the business name.",
        "Recording disclosure": "Add 'this call may be recorded' to the opener.",
        "Lead capture": "Always collect name, callback number and service address before ending.",
        "Empathy": "Acknowledge the problem first ('Sorry to hear that, let's get it sorted').",
        "Booking": "Offer two concrete time slots and confirm the booking aloud.",
        "Urgency handling": "Emergency callers need a same-day or dispatch answer.",
        "Objection/price handling": "Answer price worries with free estimate, financing or warranty.",
        "Next step stated": "Close with 'You'll get a confirmation text' or similar.",
        "No risky promises": "Avoid guarantees and exact prices before inspection.",
    }
    for n, p, m, _ in r.checks:
        if p < m:
            r.coaching.append(f"{n}: {tips[n]}")
    return r


def score_file(path):
    with open(path, encoding="utf-8") as f:
        return score(parse(f.read()), os.path.basename(path))
