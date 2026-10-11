"""Rule definitions. Pure regex, zero dependencies. Edit freely per niche."""
import re

PHONE = re.compile(r"(\+?\d[\d\-\s().]{7,}\d)")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
ADDRESS = re.compile(r"\b\d{1,5}\s+[A-Za-z0-9 .]+\s(?:street|st|road|rd|avenue|ave|drive|dr|lane|ln|court|ct|way|blvd|boulevard)\b", re.I)
NAME = re.compile(r"\b(?:my name is|this is|i am|i'm|name'?s)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)")
BOOKED = re.compile(r"\b(?:you'?re (?:all )?(?:booked|scheduled|set)|i(?:'ve| have) (?:booked|scheduled)|booked you|see you (?:on|at|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)|appointment (?:is )?(?:confirmed|set))", re.I)
TIME_OFFER = re.compile(r"\b(?:\d{1,2}(?::\d{2})?\s?(?:am|pm)|tomorrow|today|this (?:morning|afternoon|evening)|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", re.I)
EMERGENCY = re.compile(r"\b(?:leak(?:ing)?|flood(?:ed|ing)?|no (?:heat|heating|ac|cooling|hot water)|burst|emergency|urgent|gas smell|smoke|asap|right now|pain|bleeding)\b", re.I)
EMPATHY = re.compile(r"\b(?:sorry to hear|i understand|that sounds|i can imagine|no worries|happy to help|let'?s get (?:this|that) sorted|we'?ll take care)\b", re.I)
GREETING = re.compile(r"\b(?:thank you for calling|thanks for calling|good (?:morning|afternoon|evening)|hello|welcome to)\b", re.I)
NEXT_STEP = re.compile(r"\b(?:we(?:'ll| will) (?:call|text|email|send)|you(?:'ll| will) (?:get|receive)|a (?:technician|team member|specialist|estimator) will|confirmation (?:text|email))", re.I)
RECORDING = re.compile(r"\b(?:call(?:s)? (?:may be|is|are) recorded|recorded for (?:quality|training)|this call is being recorded)\b", re.I)
PRICE = re.compile(r"\b(?:how much|price|cost|quote|estimate|rates?)\b", re.I)
OBJECTION = re.compile(r"\b(?:too expensive|too much|think about it|call (?:you )?back|shop around|other quotes?|not sure|maybe later)\b", re.I)
HANDLED = re.compile(r"\b(?:free (?:estimate|quote|inspection)|no obligation|financing|payment plan|warranty|price match)\b", re.I)
UNSAFE_PROMISE = re.compile(r"\b(?:guarantee (?:you )?(?:a |the )?(?:best |perfect |full )?(?:cure|results?)|100% (?:sure|certain)|definitely (?:cost|be) \$?\d+)", re.I)
HANDOFF = re.compile(r"\b(?:transfer(?:ring)? you|let me (?:get|connect)|human|team member will call)\b", re.I)
