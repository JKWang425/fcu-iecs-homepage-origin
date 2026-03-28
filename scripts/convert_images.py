import re
from pathlib import Path
from urllib.parse import unquote
from PIL import Image

root = Path(__file__).resolve().parent.parent
html = root / "index.html"
text = html.read_text(encoding="utf-8")
srcs = set(re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', text))
media_srcs = [unquote(s) for s in srcs if s.startswith("./media/img/")]
converted = []
failed = []

for src in sorted(media_srcs):
    original = root / src[2:]
    if not original.exists():
        failed.append((src, "source missing"))
        continue
    for ext, options in [(".webp", {"quality": 75}), (".avif", {"quality": 60})]:
        target = original.with_name(original.name + ext)
        if target.exists():
            continue
        try:
            with Image.open(original) as img:
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                img.save(target, format=ext[1:].upper(), **options)
            converted.append(str(target.relative_to(root)))
        except Exception as exc:
            failed.append((str(original.relative_to(root)), str(exc)))

print("converted", len(converted))
for path in converted[:20]:
    print(path)
if failed:
    print("failed", len(failed))
    for path, reason in failed[:20]:
        print(path, reason)
