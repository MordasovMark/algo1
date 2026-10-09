"""Build site/dist/index.html from site/src/template.html and the JSON in data/.

Usage: python3 site/build.py
The template holds all CSS and JS. The data files are inlined into it so the
result is one static file that can be hosted anywhere (GitHub Pages, Netlify).
"""
import json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
data = root / 'data'
ai = root / 'ai'

def load(name):
    return json.loads((data / name).read_text(encoding='utf8'))

gem = (ai / 'gemini-gem-instructions.md').read_text(encoding='utf8').split('---', 1)[1].strip()
D = {
    'roadmap': load('roadmap.json'),
    'lc': load('leetcode.json'),
    'mcq': load('exam-mcq.json'),
    'videos': load('island-videos.json'),
    'ai': {
        'skill': (ai / 'claude-skill/pseudocode-to-leetcode/SKILL.md').read_text(encoding='utf8'),
        'gem': gem,
    },
}
blob = (json.dumps(D, ensure_ascii=False, separators=(',', ':'))
        .replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029'))
tpl = (root / 'site/src/template.html').read_text(encoding='utf8')
marker = '/*__DATA__*/null'
assert marker in tpl, 'data marker missing in template'
out = root / 'site/dist/index.html'
out.write_text(tpl.replace(marker, blob), encoding='utf8')
print('wrote', out, len(out.read_text(encoding='utf8')), 'chars')
