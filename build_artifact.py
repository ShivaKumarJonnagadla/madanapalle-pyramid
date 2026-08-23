#!/usr/bin/env python3
"""Produce a self-contained artifact.html from index.html:
   - inline every assets/img/* as a data URI
   - replace the <div class="vids">...</div> blocks with a 'videos on full site' note
"""
import base64, re, pathlib

root = pathlib.Path(__file__).parent
html = (root / "index.html").read_text(encoding="utf-8")

mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}

def inline(match):
    path = match.group(1)
    f = root / path
    if not f.exists():
        return match.group(0)
    ext = f.suffix.lower()
    b64 = base64.b64encode(f.read_bytes()).decode()
    return 'src="data:%s;base64,%s"' % (mime.get(ext, "image/jpeg"), b64)

html = re.sub(r'src="(assets/img/[^"]+)"', inline, html)

# Replace video groups with a note (videos are too large to inline)
note = ('<p style="margin:.9rem 0 0;font-size:.9rem;color:var(--accent);font-weight:600">'
        '▶ Watch the videos of this stage on the full website</p>')
html = re.sub(r'<div class="vids">.*?</div>', note, html, flags=re.DOTALL)

# Drop the single-video foundation/pillars leftover <video> tags if any remain
html = re.sub(r'<video[^>]*>\s*</video>', '', html)

(root / "artifact.html").write_text(html, encoding="utf-8")
size = (root / "artifact.html").stat().st_size
print("artifact.html written: %.2f MB" % (size / 1048576))
