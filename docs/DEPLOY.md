# פרסום חינם: Cloudflare Pages + Firebase (Spark)

הכול בחינם, בלי כרטיס אשראי (לפי התמחור שהכרתי. כדאי לוודא בדפי התמחור של הספקים).

מה שייבנה:
- **האתר** (`site/dist/index.html`) ב-Cloudflare Pages.
- **התחברות עם Google ושמירת התקדמות** ב-Firebase (Authentication + Firestore).
- **לוח מרצה** ב-`/teacher.html`.

אם לא תמלאו את `site/dist/config.js`, האתר עובד כרגיל בלי חשבונות (שמירה בדפדפן בלבד).

## שלב 1: פרויקט Firebase (10 דקות)
1. https://console.firebase.google.com ← **Add project** ← שם (למשל `algo1-voyage`) ← בלי Google Analytics ← Create.
2. **Build > Authentication > Get started > Sign-in method > Google** ← Enable ← בחרו מייל תמיכה ← Save.
3. **Build > Firestore Database > Create database** ← Production mode ← בחרו אזור קרוב (למשל `europe-west`). אי אפשר לשנות אזור אחר כך.
4. בלשונית **Rules** הדביקו את `firebase/firestore.rules` **אחרי שהחלפתם** את `LECTURER@example.com` ו-`TA@example.com` במיילי הצוות (Google) ← Publish.
5. **Project settings (גלגל שיניים) > General > Your apps > Web (</>)** ← רשמו אפליקציה ← העתיקו את אובייקט `firebaseConfig`.
6. בקובץ `site/dist/config.js` הסירו את ההערות `//` ומלאו את הערכים (apiKey, authDomain, projectId, appId). אפשר להגביל לדומיין אוניברסיטה: `allowedDomain: "hit.ac.il"` (אם הסטודנטים מתחברים עם מייל כזה). הערכים האלה **אינם סודיים**: ההגנה היא בכללי Firestore.
7. עשו commit ו-push (אפשר לערוך את הקובץ ישירות באתר GitHub).

## שלב 2: Cloudflare Pages (10 דקות)
1. https://dash.cloudflare.com ← **Workers & Pages > Create > Pages > Connect to Git** ← בחרו את הריפו `algo1`.
2. הגדרות:
   - **Production branch:** `claude/nice-pasteur-mrpjlh` (או `main` אחרי שמאחדים אליו).
   - **Framework preset:** None.
   - **Build command:** ריק.
   - **Build output directory:** `site/dist`.
3. Save and Deploy. תקבלו כתובת `משהו.pages.dev`.
   - אם האתר מחזיר 404, ה-Build output directory ריק. תקנו ב-**Settings > Build > Build configuration** ל-`site/dist` ופרסו מחדש.
   - הכתובת הנוכחית: https://algo1-bn0.pages.dev
4. חזרו ל-Firebase: **Authentication > Settings > Authorized domains > Add domain** והוסיפו את `משהו.pages.dev`. בלי זה ההתחברות לא תעבוד.

## שלב 3: בדיקה
1. פתחו את הכתובת, התחברו עם Google, פתרו שאלה, ובדקו ש-**Firestore > Data > users** מכיל מסמך עם החשבון שלכם.
2. התחברו ממכשיר אחר ובדקו שההתקדמות חוזרת.
3. פתחו `/teacher.html` עם מייל שרשום ב-`firestore.rules` ובדקו שהטבלה מופיעה.

## כשהאתר מתעדכן
- שינוי בתוכן (`data/*.json`) או בתבנית (`site/src/template.html`): הריצו `python3 site/build.py`, עשו commit ל-`site/dist/`, ו-Cloudflare יפרסם מחדש.

## מגבלות חינם שכדאי להכיר
- **Firestore (Spark):** בערך 20 אלף כתיבות ו-50 אלף קריאות ביום. האתר שומר לענן רק כל 20 שניות לכל היותר וביציאה מהדף, כדי להישאר בתוך המכסה גם עם כמה מאות סטודנטים פעילים.
- אם תחצו את המכסה, הכתיבה לענן תיכשל והשמירה בדפדפן תמשיך לעבוד.

## פרטיות (חובה לחשוב עליה)
- נשמרים: שם, מייל והתקדמות. כתבו לסטודנטים מה נשמר ולמה, ומי רואה (אתם בלבד).
- **חומר המבחנים של HIT:** לפני פרסום ציבורי קבלו אישור מהמרצה או מהפקולטה. בלי אישור, הגבילו את הגישה לסטודנטים של הקורס (`allowedDomain`) או הסירו את שאלות המבחן.
- **מחיקת חשבון:** הכללים מאפשרים לסטודנט למחוק את המסמך שלו, אבל עדיין אין כפתור באתר. כרגע מוחקים ידנית ב-Firestore לפי בקשה.
