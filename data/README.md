# Content data (Step 2 input)

| File | What |
|---|---|
| `roadmap.json` | Weeks, nodes and edges of the roadmap. Nodes with `"proposed": true` are not in the syllabus you sent but appear in past exams. |
| `leetcode.json` | Easy-only LeetCode questions per node, with a Hebrew/English title, a short paraphrased statement and a Hebrew explanation. Links go out to LeetCode. |
| `judge.json` | Specs and tests for the in-site judge ("Solve here"), keyed by LeetCode number. Each has a reference solution in `judge/solutions/<n>.py`; `site/build.py` refuses to build if one fails its tests. Tests are our own, not LeetCode's. |
| `exam-mcq.json` | Multiple-choice questions derived from the 2022-2024 exams. `basis: official-solution` = the answer matches a solution that was in the PDFs; `basis: derived` = worked out without an official solution, needs a TA check before publishing. |

The exam PDFs themselves are not committed (they are HIT material).
