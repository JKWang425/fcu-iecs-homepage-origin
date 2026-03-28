import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / 'index.html'
text = path.read_text(encoding='utf-8')

pattern = re.compile(r'<img[^>]*>')


def repl(match):
    tag = match.group(0)
    if 'class="' not in tag:
        return tag
    class_attr = re.search(r'class="([^"]*)"', tag)
    if not class_attr:
        return tag
    classes = class_attr.group(1)
    if 'd-block' not in classes or 'w-100' not in classes:
        return tag
    if 'loading=' in tag or 'fetchpriority=' in tag:
        return tag
    if tag.endswith('/>'):
        return tag[:-2] + ' loading="lazy"/>'
    return tag[:-1] + ' loading="lazy">'

new_text = pattern.sub(repl, text)
if new_text != text:
    path.write_text(new_text, encoding='utf-8')
    print('updated')
else:
    print('no changes')
