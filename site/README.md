# Site: מסע האלגוריתמים

One static HTML file with the roadmap, exam multiple-choice questions, LeetCode lists, visualizations and the 30-minute workflow.

- `src/template.html`: all CSS and JavaScript (the source of truth).
- `build.py`: inlines `data/*.json` and `ai/*` into the template. Run `python3 site/build.py`.
- `dist/index.html`: the built page. Host it as is.
- `src/judge.py`: the judge harness for "Solve here". It runs in the browser (Pyodide in a Web Worker, so no server) and at build time, where `build.py` runs every reference solution through it.
- `tests/smoke.js`: opens all 70 LeetCode visualizations headlessly.
- `tests/judge.js`: submits each reference solution and each empty starter in a real browser, and checks the time limit.

Progress is stored only in each browser's localStorage. There is no backend.
