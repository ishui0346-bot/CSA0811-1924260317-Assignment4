"""Validation of one registration line:  regno;name;email;event   (string methods only)."""
from .errors import InvalidRegistration

EMAIL_LOCAL_EXTRA = set("._%+-")          # punctuation allowed in the part before @
FIELDS = 4

def is_valid_email(email):
    """True if email looks valid. Rules (string methods only):
    exactly one '@'; no spaces; local part and domain not empty; local part only letters, digits and . _ % + -
    and not starting/ending with '.' or containing '..'; domain contains a '.', its labels are not empty,
    made of letters, digits or '-'; the last label (e.g. 'edu') is at least 2 letters."""
    if email.count("@") != 1 or " " in email:
        return False
    local, domain = email.split("@")
    if not local or not domain:
        return False
    if local.startswith(".") or local.endswith(".") or ".." in local:
        return False
    if not all(ch.isalnum() or ch in EMAIL_LOCAL_EXTRA for ch in local):
        return False
    if "." not in domain or domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    labels = domain.split(".")
    if not all(label and all(ch.isalnum() or ch == "-" for ch in label) for label in labels):
        return False
    return len(labels[-1]) >= 2 and labels[-1].isalpha()

def validate_line(line, line_no):
    """Return a dict {regno, name, email, event} (normalised) or raise InvalidRegistration."""
    text = line.strip()
    if text == "":
        raise InvalidRegistration(line_no, text, "empty line")
    parts = [p.strip() for p in text.split(";")]
    if len(parts) != FIELDS:
        raise InvalidRegistration(line_no, text, f"expected {FIELDS} fields separated by ';', found {len(parts)}")
    regno, name, email, event = parts
    if not (len(regno) == 9 and regno.isdigit() and regno.isascii()):
        raise InvalidRegistration(line_no, text, f"register number {regno!r} must be 9 digits")
    name = " ".join(name.split())                     # collapse repeated spaces
    if not name:
        raise InvalidRegistration(line_no, text, "name is empty")
    email = email.lower()
    if not is_valid_email(email):
        raise InvalidRegistration(line_no, text, f"invalid email {parts[2]!r}")
    event = " ".join(event.split())
    if not event:
        raise InvalidRegistration(line_no, text, "event is empty")
    return {"regno": regno, "name": name.title(), "email": email, "event": event.title()}

def duplicate_key(record):
    """Two registrations are duplicates if the same register number registers for the same event (case-insensitive)."""
    return (record["regno"], record["event"].lower())
