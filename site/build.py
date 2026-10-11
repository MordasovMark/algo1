"""Build site/dist/index.html from site/src/template.html and the JSON in data/.

Usage: python3 site/build.py
The template holds all CSS and JS. The data files are inlined into it so the
result is one static file that can be hosted anywhere (GitHub Pages, Netlify).
"""
import json, pathlib, importlib.util, sys

root = pathlib.Path(__file__).resolve().parent.parent
data = root / 'data'
ai = root / 'ai'

def load(name):
    return json.loads((data / name).read_text(encoding='utf8'))

def check_judge(judge, lc_numbers):
    """Run each reference solution through the same harness the browser uses."""
    spec_ = importlib.util.spec_from_file_location('judge', root / 'site/src/judge.py')
    h = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(h)
    bad = []
    for n, spec in judge['problems'].items():
        if int(n) not in lc_numbers:
            bad.append(f'{n}: not in leetcode.json')
            continue
        spec['starter'] = h.starter(spec)
        src = (data / 'judge/solutions' / f'{n}.py').read_text(encoding='utf8')
        events = []
        res = json.loads(h.judge(src, json.dumps(dict(spec, stopOnFail=False)), events.append))
        results = [json.loads(e)['result'] for e in events if 'result' in json.loads(e)]
        for r in results:
            if not r['ok']:
                bad.append(f"{n} test {r['i']}: {r.get('error') or 'got ' + r['got'] + ', want ' + r['want']}")
            elif r['ms'] > spec['limitMs'] / 4:
                print(f"warning: {n} test {r['i']} took {r['ms']} ms in CPython (limit {spec['limitMs']} ms in the browser)")
        if res['verdict'] != 'AC' or len(results) != len(spec['tests']):
            bad.append(f"{n}: reference verdict {res['verdict']}, ran {len(results)}/{len(spec['tests'])} tests")
        if json.loads(h.judge(spec['starter'] + 'pass\n', json.dumps(spec), lambda e: None))['verdict'] == 'AC':
            bad.append(f'{n}: the empty starter is accepted, the tests are too weak')
    if bad:
        sys.exit('judge check failed:\n  ' + '\n  '.join(bad))
    print('judge: checked', len(judge['problems']), 'problems')
    judge['harness'] = (root / 'site/src/judge.py').read_text(encoding='utf8')
    return judge

gem = (ai / 'gemini-gem-instructions.md').read_text(encoding='utf8').split('---', 1)[1].strip()
D = {
    'roadmap': load('roadmap.json'),
    'lc': load('leetcode.json'),
    'mcq': load('exam-mcq.json'),
    'videos': load('island-videos.json'),
    'open': load('exam-open.json'),
    'judge': None,
    'ai': {
        'skill': (ai / 'claude-skill/pseudocode-to-leetcode/SKILL.md').read_text(encoding='utf8'),
        'gem': gem,
    },
}
D['judge'] = check_judge(load('judge.json'), {q['number'] for q in D['lc']['questions']})
blob = (json.dumps(D, ensure_ascii=False, separators=(',', ':'))
        .replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029'))
tpl = (root / 'site/src/template.html').read_text(encoding='utf8')
marker = '/*__DATA__*/null'
assert marker in tpl, 'data marker missing in template'
out = root / 'site/dist/index.html'
out.write_text(tpl.replace(marker, blob), encoding='utf8')
print('wrote', out, len(out.read_text(encoding='utf8')), 'chars')

# Small lookup used by teacher.html (question text and node per MCQ id).
meta = {'mcq': [{'id': q['id'], 'node': q['node'], 'stem': q['stem']['he']} for q in D['mcq']['questions']]}
(root / 'site/dist/data.json').write_text(json.dumps(meta, ensure_ascii=False), encoding='utf8')
print('wrote site/dist/data.json')
