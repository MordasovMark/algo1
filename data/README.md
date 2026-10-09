# Content data (Step 2 input)

| File | What |
|---|---|
| `roadmap.json` | Weeks, nodes and edges of the roadmap. Nodes with `"proposed": true` are not in the syllabus you sent but appear in past exams. |
| `leetcode.json` | Easy-only LeetCode questions per node, with a Hebrew/English title, a short paraphrased statement and a Hebrew explanation. Links go out to LeetCode. |
| `exam-mcq.json` | Multiple-choice questions derived from the 2022-2024 exams. `basis: official-solution` = the answer matches a solution that was in the PDFs; `basis: derived` = worked out without an official solution, needs a TA check before publishing. |

The exam PDFs themselves are not committed (they are HIT material).
