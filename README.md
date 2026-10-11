# המסע אל עבר הארגזים

אתר תרגול לקורס אלגוריתמים 1 (HIT): מפת מסע לפי שבועות, עם שאלות LeetCode ברמת Easy, הסברים ותרגום לעברית, ויזואליזציות ושאלות ממבחני עבר.

**לאתר: https://algo1-bn0.pages.dev**

אהבתם? תנו ⭐ לריפו. זה עוזר לסטודנטים אחרים למצוא את האתר.

## מה יש באתר
- איים לפי שבועות הקורס. כל אי נפתח בוויזואליזציה של האלגוריתם ובסרטון מומלץ.
- 35 שאלות LeetCode ברמת Easy, עם תרגום לעברית, הסבר, ושתי ויזואליזציות לכל שאלה: הרעיון והפתרון.
- המלצה איך לעבוד על שאלה: קודם לבד, אחר כך סרטון, ורק בסוף AI. הכול פתוח, בלי מנעולים.
- שאלות אמריקאיות ושאלות פתוחות ממבחני 2022–2024. הפתרון נחשף רק אחרי ניסיון.
- כרטיס "היום" עם פעולה אחת ברורה, יעד XP יומי, רצף ימים וספירה לאחור למבחן עם קצב מומלץ.
- חזרה מרווחת: כל שאלה חוזרת אחרי 1, 3, 7, 16 ו-35 ימים.
- תזכורת יומית ביומן (Google או קובץ ‎.ics) והתקנה כאפליקציה בטלפון (PWA).
- התחברות עם Google, שמירת ההתקדמות בענן וסנכרון בין מכשירים (לא חובה).

שאלות שמסומנות "טיוטה" עדיין לא נבדקו על ידי מתרגל. מצאתם טעות? פתחו [Issue](https://github.com/MordasovMark/algo1/issues).

## מבנה הריפו
| תיקייה | תוכן |
|---|---|
| `data/` | התוכן: מפת הדרכים, שאלות LeetCode, שאלות מבחן וסרטונים |
| `site/src/template.html` | הקוד של האתר (HTML/CSS/JS בקובץ אחד) |
| `site/build.py` | בונה את `site/dist/index.html` מהתבנית ומהנתונים |
| `site/dist/` | האתר המוכן, שמתפרסם ב-Cloudflare Pages |
| `firebase/` | חוקי האבטחה של Firestore |
| `ai/` | פרומפטים שמתרגמים פסאודו-קוד לפייתון בכלי AI חיצוני |
| `docs/DEPLOY.md` | איך לפרסם בחינם (Cloudflare Pages + Firebase Spark) |

## הרצה מקומית
```bash
python3 site/build.py
# open site/dist/index.html
```

---

**English:** A practice site for the HIT Algorithms 1 course: a week-by-week map with Easy LeetCode questions (Hebrew translations and explanations), visualizations and past-exam questions. Live at https://algo1-bn0.pages.dev. If it helps you, a ⭐ is appreciated.
