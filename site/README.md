# Site: מסע האלגוריתמים

One static HTML file with the roadmap, exam multiple-choice questions, LeetCode lists, visualizations and the 30-minute workflow.

- `src/template.html`: all CSS and JavaScript (the source of truth).
- `build.py`: inlines `data/*.json` and `ai/*` into the template. Run `python3 site/build.py`.
- `dist/index.html`: the built page. Host it as is.
- `tests/smoke.js`: opens all 70 LeetCode visualizations headlessly.

Progress is stored only in each browser's localStorage. There is no backend.
