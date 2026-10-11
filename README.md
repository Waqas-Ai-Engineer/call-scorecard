# call-scorecard

> Score AI-receptionist and front-desk call transcripts for lead capture, booking, empathy and compliance - one command, zero dependencies, works offline.

![python](https://img.shields.io/badge/python-3.8%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![deps](https://img.shields.io/badge/dependencies-0-brightgreen) ![tests](https://img.shields.io/badge/tests-6%20passing-brightgreen)

## Quickstart (under 2 minutes)

```bash
git clone https://github.com/Waqas-Ai-Engineer/call-scorecard
cd call-scorecard
python -m callscore examples/calls                       # text scorecard
python -m callscore examples/calls --format html --out report.html
python -m callscore examples/calls --min-score 70        # exit 1 in CI if any call is below 70
```

## Problem

Roofing, HVAC, clinic and salon owners pay for AI receptionists or answering services but never know if calls actually turn into bookings. Reading transcripts by hand does not scale.

## Solution

`call-scorecard` reads transcripts (`Agent:` / `Caller:` lines, or a JSON list of `{role,text}`) and scores each call out of 100 with plain-language coaching tips.

## Features

- 9 explainable checks: greeting, recording disclosure, lead capture (name/phone/address/email), empathy, booking, urgency handling, price-objection handling, next step, risky promises
- Detects emergency callers (leaks, no heat, floods) and checks for same-day handling
- Text, JSON and HTML reports; `--min-score` exit code for CI or n8n "Execute Command" nodes
- Rules are plain regex in `callscore/rules.py` - tune per niche or language
- Offline, deterministic, no API keys

## Example output

```
hvac_good.txt: 100/100 [A] outcome=booked  URGENT
   ok Greeting                    5/5
   ok Recording disclosure        5/5
   ok Lead capture               27/27
   ok Empathy                     8/8
   ok Booking                    25/25
   ok Urgency handling           10/10
   ok Objection/price handling   10/10
   ok Next step stated            5/5
   ok No risky promises           5/5

roofing_poor.txt: 5/100 [F] outcome=no_booking  URGENT
   ok Greeting                    5/5
   -- Recording disclosure        0/5
   -- Lead capture                0/27
   -- Empathy                     0/8
   -- Booking                     0/25
   -- Urgency handling            0/10
   -- Objection/price handling    0/10
   -- Next step stated            0/5
   -- No risky promises           0/5
   tip: Recording disclosure: Add 'this call may be recorded' to the opener.
   tip: Lead capture: Always collect name, callback number and service address before ending.
   tip: Empathy: Acknowledge the problem first ('Sorry to hear that, let's get it sorted').
```

## Architecture

```
transcript (.txt/.json) -> parse() -> turns -> score() -> checks + coaching -> text | json | html
                                          ^ rules.py (regex rules)
```

## How it works

Each check awards points (max 100). Rule-based scoring is transparent and cheap; it is a heuristic, not a replacement for human QA. Pair it with an LLM judge for nuance if you need one.

## Use with n8n

Use an Execute Command node: `python -m callscore /data/calls --format json`, then branch on score to alert the owner about low-scoring or unbooked emergency calls.

## Project structure

```
callscore/   scorer.py rules.py report.py cli.py
tests/       unittest suite
examples/    sample HVAC / roofing / salon transcripts (synthetic)
```

## Honesty note

Sample transcripts are synthetic. No real customer data, users or metrics are claimed.

## Future improvements

Optional LLM judge, speech-to-text input, multilingual rules, CSV export.

## Hire me / Need this built?

Need AI call handling, lead capture or CRM automation for your business? I'm **Muhammad Waqas - AI Agents & Business Automation**. Reach me via my [GitHub profile](https://github.com/Waqas-Ai-Engineer).

## License

MIT
