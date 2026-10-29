#!/usr/bin/env python3
"""Build docs/index.html from src/.

Edit content in src/screens.json (one object per screen) and the look or behaviour
in src/template_head.html (HTML head + CSS) and src/app.html (JavaScript).
Then run:  python3 build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SRC, OUT = ROOT / "src", ROOT / "docs"

screens = json.loads((SRC / "screens.json").read_text(encoding="utf-8"))
meta = json.loads((SRC / "meta.json").read_text(encoding="utf-8"))

# Basic checks so a typo in screens.json fails loudly instead of breaking the page.
ids = set()
for s in screens:
    for key in ("id", "group", "title", "icon", "path", "summary", "mod", "roles"):
        if key not in s:
            raise SystemExit(f"Screen {s.get('id', '?')} is missing '{key}'")
    if s["id"] in ids:
        raise SystemExit(f"Duplicate screen id: {s['id']}")
    ids.add(s["id"])
    if s.get("img") and not (OUT / "img" / f"{s['img']}.jpg").exists():
        raise SystemExit(f"Screen {s['id']} points to a missing image docs/img/{s['img']}.jpg")
    known = {m[0] for m in meta["modules"]} | {"base"}
    if s["mod"] not in known:
        raise SystemExit(f"Screen {s['id']} has unknown module '{s['mod']}'")

def as_json(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

template = (SRC / "template_head.html").read_text(encoding="utf-8") + (SRC / "app.html").read_text(encoding="utf-8")
html = template.replace("__DATA__", as_json(screens)).replace("__META__", as_json(meta))
(OUT / "index.html").write_text(html, encoding="utf-8")
print(f"Built docs/index.html: {len(screens)} screens, {len(html):,} bytes")
