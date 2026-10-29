# Reference only: turned the raw demo-site capture (not included in this repo) into src/screens.json.
# Day-to-day edits go in src/screens.json; rebuild with ../build.py.
import re

MARKERS = [
    ("next", r"DO THIS NEXT"),
    ("can", r"What you can do here"),
    ("concepts", r"Key concepts"),
    ("rules", r"Important rules"),
    ("tips", r"Tips to go faster"),
    ("watch", r"Watch out for"),
]
ICON_WORDS = {"close", "arrow_circle_right", "checklist", "menu_book", "policy", "bolt",
              "error_outline", "tips_and_updates", "Close"}


def parse_guide(text):
    """Split the in-app guide panel text into sections."""
    if not text:
        return {}
    text = re.sub(r"tips_and_updates[\s\S]*$", "", text)
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    out = {"title": "", "summary": ""}
    # header: "XXX GUIDE", title, summary
    i = 0
    if lines and lines[0].isupper() and "GUIDE" in lines[0]:
        i = 1
    hdr = []
    while i < len(lines) and lines[i] not in ICON_WORDS and not any(re.fullmatch(m, lines[i]) for _, m in MARKERS):
        hdr.append(lines[i]); i += 1
    if hdr:
        out["title"] = hdr[0]
        out["summary"] = " ".join(hdr[1:])
    cur = None
    for l in lines[i:]:
        hit = [k for k, m in MARKERS if re.fullmatch(m, l)]
        if hit:
            cur = hit[0]; out[cur] = []; continue
        if l in ICON_WORDS or cur is None:
            continue
        out[cur].append(l)
    # concepts come in pairs (term, definition)
    if out.get("concepts"):
        c = out["concepts"]; pairs = []
        for j in range(0, len(c) - 1, 2):
            pairs.append([c[j], c[j + 1]])
        if len(c) % 2:
            pairs.append([c[-1], ""])
        out["concepts"] = pairs
    if out.get("next"):
        out["next"] = " ".join(out["next"])
    return out


def parse_form(text):
    """Turn a dialog's text into [{'step':..,'sub':..,'fields':[{label,hint,req}]}]."""
    if not text or text.startswith("[no dialog]"):
        return []
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    lines = [l for l in lines if l not in ("close", "Save", "Cancel", "Update", "Submit", "Reset")]
    if lines and not re.fullmatch(r"\d+", lines[0]):
        lines = lines[1:]  # dialog title
    steps = []
    cur = None
    k = 0
    while k < len(lines):
        l = lines[k]
        if re.fullmatch(r"\d{1,2}", l) and k + 1 < len(lines):
            cur = {"step": lines[k + 1], "sub": "", "fields": []}
            if k + 2 < len(lines) and lines[k + 2][:1].islower() and not lines[k + 2].endswith("."):
                cur["sub"] = lines[k + 2]; k += 1
            steps.append(cur); k += 2; continue
        if cur is None:
            cur = {"step": "Details", "sub": "", "fields": []}; steps.append(cur)
        is_hint = l.endswith(".") or l.endswith(".)")
        if is_hint and cur["fields"]:
            cur["fields"][-1]["hint"] = (cur["fields"][-1].get("hint", "") + " " + l).strip()
        elif len(l) > 90:
            if cur["fields"]:
                cur["fields"][-1]["hint"] = (cur["fields"][-1].get("hint", "") + " " + l).strip()
        elif re.fullmatch(r"[a-z_]+", l):
            pass  # material icon name
        else:
            req = l.endswith("*")
            cur["fields"].append({"label": l.rstrip(" *"), "req": req})
        k += 1
    # drop pure value lines that precede a dropdown label (e.g. "Permanent(P)") - keep as default
    for s in steps:
        cleaned = []
        for f in s["fields"]:
            cleaned.append(f)
        s["fields"] = cleaned
    return [s for s in steps if s["fields"]]
