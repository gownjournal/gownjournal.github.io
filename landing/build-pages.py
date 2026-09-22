# -*- coding: utf-8 -*-
"""Generate the segment landing pages from one shared design system.

Every page here is a standalone .html for embedding or hosting, but they all
draw their CSS and their business facts from the same place, so a change to the
look or to the address happens once rather than per file.

    python3 build-pages.py
"""
import re, json, pathlib

BASE = pathlib.Path(__file__).parent
SRC  = (BASE / 'shany-sasson-fitting.html').read_text(encoding='utf-8')
STYLE = re.search(r'<style>.*?</style>', SRC, re.S).group(0)
FONTS = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis[^>]*>', SRC).group(0)
WA_SVG = re.search(r'<svg viewBox="0 0 24 24" aria-hidden="true">.*?</svg>', SRC, re.S).group(0)

# ---- business facts: one source, per the skill's brand-facts reference ----
WA, TEL = "972525557106", "+972525557106"
HERO = ('https://static.wixstatic.com/media/86c7d2_e659073414514023ac52e7cb4346bd0b~mv2.jpg'
        '/v1/fill/w_1200,h_630,al_t,q_85/file.jpg')
LOGO = 'https://cdn.shopify.com/s/files/1/0749/3658/2189/files/logo_Shany_Sasson_transpert_2.png?v=1776603856'
MAPQ = ('https://www.google.com/maps/search/?api=1&amp;query='
        '%D7%A2%D7%99%D7%9F+%D7%97%D7%99+7+%D7%94%D7%95%D7%93+%D7%94%D7%A9%D7%A8%D7%95%D7%9F')

def gown(h, w=760, ht=1140):
    return f'https://static.wixstatic.com/media/86c7d2_{h}~mv2.jpg/v1/fill/w_{w},h_{ht},al_c,q_80/file.jpg'

G = {'vintage':'47da3cd9a54d4bde82c5e549edd25323','heart':'b35c5c25433945cda57d59620f827892',
     'chiffon':'e659073414514023ac52e7cb4346bd0b','train':'a7f905db0a5840369ce15339eb1796ad',
     'aline':'254d9a96e910476799df4b60b0d571fd','openback':'38a7475f3ddc438b8a3d045469d4d4df',
     'sleeves':'ffdac4e521d0492bb1f146068949cc8f'}

BIZ = {"@context":"https://schema.org","@type":["LocalBusiness","ClothingStore"],
 "@id":"https://www.shanysasson.com/#studio","name":"שני ששון שמלות כלה",
 "alternateName":"Lace & Love by Shany Sasson","url":"https://www.shanysasson.com/","image":HERO,"logo":LOGO,
 "telephone":"+972-52-555-7106","email":"shanysasson@gmail.com","inLanguage":"he-IL",
 "address":{"@type":"PostalAddress","streetAddress":"עין חי 7","addressLocality":"הוד השרון","addressCountry":"IL"},
 "founder":{"@type":"Person","name":"שני ששון","jobTitle":"מעצבת שמלות כלה"},
 "areaServed":[{"@type":"Country","name":"ישראל"},{"@type":"Country","name":"ארצות הברית"},{"@type":"Place","name":"אירופה"}],
 "sameAs":["https://www.instagram.com/lace_and_love_brides/",
           "https://www.facebook.com/shanysasson.bridal.fashion.home",
           "https://www.pinterest.com/LaceandLoveBrides",
           "https://shany-sasson-wedding-dresses.com/"]}

# verbatim, from the owner's Google Business Profile — the only quotable set
REVIEWS = [("ליאור דגן","2026","ממש נוח שאפשר להתבסס על דגם ששני עיצבה ולהתאים אותו בדיוק אלייך בתפירה הייחודית שלה. לכל מי שמתחברת לסגנון הבוהו-שיק, תחרה ולמראה הרומנטי, אמליץ בחום."),
           ("אביה פלד","2026","מהרגע הראשון שנכנסתי לסטודיו הרגשתי בידיים הכי טובות שיש. שני קשובה, סבלנית, יצירתית, מקצועית ומשרה המון רוגע בתקופה הלחוצה הזו."),
           ("עדי","2019","שני הייתה נעימה וסבלנית כבר מהפעם הראשונה שנכנסנו לסטודיו שלה. בכל מדידה היא הייתה מדייקת, מקצועית ונעימה, והתוצאה הייתה מהממת - שמלה מותאמת ומעוצבת במיוחד בשבילי.")]

def ld(o): return '<script type="application/ld+json">\n'+json.dumps(o,ensure_ascii=False,indent=2)+'\n</script>'

def quotes():
    rows = "\n".join(
f'''        <li class="quote">
          <p class="stars" aria-label="חמישה כוכבים מתוך חמישה">★★★★★</p>
          <blockquote>{t}</blockquote>
          <p class="cite">{n} <span>· {y}</span></p>
        </li>''' for n,y,t in REVIEWS)
    return f'''  <section class="band band-grey">
    <div class="wrap">
      <div class="band-head">
        <p class="eyebrow">מה כלות כותבות</p>
        <h2>ביקורות מ-Google</h2>
      </div>
      <ul class="quotes">
{rows}
      </ul>
    </div>
  </section>'''

def faq(pairs, eyebrow, heading):
    items = "\n".join(
f'''        <details{" open" if i==0 else ""}>
          <summary>{q}</summary>
          <p>{a}</p>
        </details>''' for i,(q,a) in enumerate(pairs))
    return f'''  <section class="band">
    <div class="wrap">
      <div class="band-head center">
        <p class="eyebrow">{eyebrow}</p>
        <h2>{heading}</h2>
      </div>
      <div class="faq">
{items}
      </div>
    </div>
  </section>'''

def faq_schema(pairs):
    return {"@context":"https://schema.org","@type":"FAQPage","inLanguage":"he-IL",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}}
                          for q,a in pairs]}

def cta(lede):
    return f'''  <section class="band band-cta" id="פגישה">
    <div class="wrap cta-grid">
      <div>
        <p class="eyebrow">קביעת פגישה</p>
        <h2>בואי למדוד.</h2>
        <p class="lede">{lede}</p>
        <ul class="contact">
          <li><span class="c-k">טלפון</span><a href="tel:{TEL}" dir="ltr">052-555-7106</a></li>
          <li><span class="c-k">הסטודיו</span><a href="{MAPQ}" target="_blank" rel="noopener">עין חי 7, הוד השרון</a></li>
          <li><span class="c-k">אימייל</span><a href="mailto:shanysasson@gmail.com" dir="ltr">shanysasson@gmail.com</a></li>
        </ul>
      </div>
      <form class="form" id="lead-form" novalidate>
        <div class="field"><label for="f-name">שם מלא</label><input id="f-name" type="text" autocomplete="name" required></div>
        <div class="field"><label for="f-phone">טלפון</label><input id="f-phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" required></div>
        <div class="field"><label for="f-date">תאריך החתונה (אם ידוע)</label><input id="f-date" type="text" placeholder="לדוגמה: מאי 2027"></div>
        <div class="field"><label for="f-note">משהו שכדאי שנדע?</label><textarea id="f-note" rows="2"></textarea></div>
        <button class="btn" type="submit">{WA_SVG}שליחה בוואטסאפ</button>
        <p class="form-note" id="form-msg">הכפתור פותח וואטסאפ עם הפרטים שמילאת, מוכנים לשליחה.</p>
      </form>
    </div>
  </section>'''

FORM_JS = '''<script>
(function(){
  var WA = "%s";
  var form = document.getElementById("lead-form"), msgEl = document.getElementById("form-msg");
  if(!form || !msgEl) return;
  var elName=document.getElementById("f-name"), elPhone=document.getElementById("f-phone"),
      elDate=document.getElementById("f-date"), elNote=document.getElementById("f-note");
  form.addEventListener("submit", function(e){
    e.preventDefault();
    var name=elName.value.trim(), phone=elPhone.value.trim(),
        date=elDate.value.trim(), note=elNote.value.trim();
    if(!name || !phone){
      msgEl.textContent = "צריך שם וטלפון כדי שנוכל לחזור אלייך.";
      (!name ? elName : elPhone).focus(); return;
    }
    var lines = ["היי שני, אשמח לקבוע פגישת מדידה.", "שם: " + name, "טלפון: " + phone];
    if(date) lines.push("תאריך החתונה: " + date);
    if(note) lines.push("הערה: " + note);
    window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent(lines.join("\\n")), "_blank", "noopener");
    msgEl.textContent = "נפתח וואטסאפ עם הפרטים, נשאר רק ללחוץ שליחה.";
  });
})();
</script>''' % WA

def page(title, desc, blocks, extra_ld):
    return f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="שני ששון שמלות כלה">
<meta property="og:image" content="{HERO}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="שמלת כלה בוהו מהסטודיו של שני ששון">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{HERO}">
<!-- Set the canonical URL once this page has its final address:
     <link rel="canonical" href="https://your-domain/your-path"> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{FONTS}
{extra_ld}
{STYLE}
</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="#top">
      <img class="brand-logo" src="https://cdn.shopify.com/s/files/1/0749/3658/2189/files/logo_Shany_Sasson_transpert_2.png?v=1776603856&amp;width=120" alt="" width="40" height="40">
      <span class="brand-text">
        <span class="brand-name">שני ששון</span>
        <span class="brand-sub">שמלות כלה · בוהו שיק</span>
      </span>
    </a>
    <a class="btn" href="#פגישה">קביעת פגישה</a>
  </div>
</header>
<main id="top">
{blocks}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <p class="footer-brand">שני ששון</p>
        <p>שמלות כלה בוהו שיק, מעוצבות ונתפרות בסטודיו בהוד השרון.</p>
      </div>
      <div>
        <p class="footer-head">הסטודיו</p>
        <ul>
          <li><a href="{MAPQ}" target="_blank" rel="noopener">עין חי 7, הוד השרון</a></li>
          <li><a href="tel:{TEL}" dir="ltr">052-555-7106</a></li>
          <li><a href="mailto:shanysasson@gmail.com" dir="ltr">shanysasson@gmail.com</a></li>
        </ul>
      </div>
      <div>
        <p class="footer-head">עוד</p>
        <ul>
          <li><a href="https://www.instagram.com/lace_and_love_brides/" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="https://www.shanysasson.com/" target="_blank" rel="noopener">האתר המלא</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom"><p>שני ששון · שמלות כלה בוהו שיק</p></div>
  </div>
</footer>
<div class="mobar">
  <a class="btn" href="https://wa.me/{WA}?text=%D7%94%D7%99%D7%99%20%D7%A9%D7%A0%D7%99%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%95%D7%A2%20%D7%A4%D7%92%D7%99%D7%A9%D7%AA%20%D7%9E%D7%93%D7%99%D7%93%D7%94" target="_blank" rel="noopener">וואטסאפ</a>
  <a class="btn btn-secondary" href="tel:{TEL}">חיוג</a>
</div>
{FORM_JS}
</body>
</html>
'''

# ======================= PAGE 1 — the city page =======================
# Local intent. Nobody in the research held "סטודיו שמלות כלה בהוד השרון",
# while competitors hold their own city terms, so this is an open query.

P1_FAQ = [
 ("צריך לתאם פגישה מראש?",
  "כן. הסטודיו עובד בתיאום בלבד, כדי שהשעה תהיה שלך ולא תתחלק בין כמה כלות. הודעה בוואטסאפ היא הדרך המהירה לתאם."),
 ("כמה זמן נמשכת הפגישה?",
  "כשעה. מספיק זמן כדי למדוד כמה דגמים, לקחת מידות ולדבר, בלי להרגיש שממהרים אותך."),
 ("אפשר להביא מלווים?",
  "בהחלט, ומומלץ. רק עדכני כמה אתן מגיעות כשנקבע, כדי שנשריין מספיק זמן ומקום."),
]

P1 = page(
 "סטודיו שמלות כלה בהוד השרון · שני ששון",
 "סטודיו שמלות כלה בוהו בעין חי 7, הוד השרון. כל שמלה מעוצבת ונתפרת בסטודיו לפי המידות שלך. פגישת מדידה ללא תשלום.",
 f'''  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">עין חי 7, הוד השרון</p>
        <h1>סטודיו שמלות כלה <em>בהוד השרון</em></h1>
        <p class="lede">
          הסטודיו של שני ששון נמצא בעין חי 7. כל שמלה שיוצאת ממנו מעוצבת ונתפרת כאן,
          לפי המידות שלך ולפי הוויב שלך. אפשר להגיע, למדוד ולהחליט אחר כך.
        </p>
        <div class="btn-row">
          <a class="btn" href="https://wa.me/{WA}?text=%D7%94%D7%99%D7%99%20%D7%A9%D7%A0%D7%99%2C%20%D7%90%D7%A9%D7%9E%D7%97%20%D7%9C%D7%A7%D7%91%D7%95%D7%A2%20%D7%A4%D7%92%D7%99%D7%A9%D7%94%20%D7%91%D7%A1%D7%98%D7%95%D7%93%D7%99%D7%95" target="_blank" rel="noopener">{WA_SVG}לקבוע פגישה בוואטסאפ</a>
          <a class="btn btn-secondary" href="{MAPQ}" target="_blank" rel="noopener">לפתוח במפות</a>
        </div>
        <dl class="facts">
          <div><dt>כתובת</dt><dd>עין חי 7</dd></div>
          <div><dt>סגנון</dt><dd>בוהו שיק</dd></div>
          <div><dt>פגישה</dt><dd>ללא תשלום</dd></div>
        </dl>
      </div>
      <figure class="hero-figure">
        <img src="{gown(G['chiffon'],1000,1500)}" alt="שמלת כלה בוהו מתחרה ושיפון מהסטודיו בהוד השרון" width="1000" height="1500" fetchpriority="high">
        <figcaption>כל שמלה בעמוד הזה נתפרת בסטודיו בעין חי 7.</figcaption>
      </figure>
    </div>
  </section>

  <section class="band band-grey">
    <div class="wrap">
      <div class="band-head">
        <p class="eyebrow">הגעה</p>
        <h2>איפה הסטודיו ואיך מגיעים אליו?</h2>
        <p class="lede">
          הכתובת היא <strong>עין חי 7, הוד השרון</strong>. הסטודיו יושב במרכז השרון,
          נסיעה קצרה מרעננה, כפר סבא, רמת השרון, הרצליה וראש העין.
        </p>
      </div>
      <div class="pillars">
        <article class="pillar">
          <span class="pillar-badge">כתובת</span>
          <h3>עין חי 7, הוד השרון</h3>
          <p>הסטודיו עבר לעין חי 7. אם ראית כתובת אחרת באחד ממאגרי האינטרנט, זו הישנה.</p>
          <p><a href="{MAPQ}" target="_blank" rel="noopener">לפתוח ניווט</a></p>
        </article>
        <article class="pillar">
          <span class="pillar-badge">תיאום</span>
          <h3>בתיאום מראש בלבד</h3>
          <p>כך השעה מוקדשת רק לך. הודעה אחת בוואטסאפ ל-<a href="tel:{TEL}" dir="ltr">052-555-7106</a> וקבענו.</p>
        </article>
        <article class="pillar">
          <span class="pillar-badge">משך</span>
          <h3>כשעה בסטודיו</h3>
          <p>מספיק כדי למדוד כמה דגמים, לקחת מידות ולהבין מה אפשר לשנות בכל שמלה.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="band-head">
        <p class="eyebrow">הפגישה</p>
        <h2>מה קורה בפגישה בסטודיו?</h2>
        <p class="lede">הפגישה הראשונה היא היכרות ומדידה. בלי לחץ של מכירה, ובלי תשלום.</p>
      </div>
      <ol class="stages">
        <li><span class="stage-n">01</span><div>
          <h3>מדידה ראשונה</h3>
          <p>את מודדת דגמים מהסטודיו, אנחנו מבינים יחד איזו גזרה הכי מחמיאה לך ולוקחים את המידות המלאות.</p>
        </div></li>
        <li><span class="stage-n">02</span><div>
          <h3>מדידת התאמה</h3>
          <p>השמלה כבר תפורה לפי המידות שלך. כאן אנחנו מדייקים את קו החזה, האורך והגב.</p>
        </div></li>
        <li><span class="stage-n">03</span><div>
          <h3>מדידה אחרונה</h3>
          <p>התאמות אחרונות עם הנעליים שתנעלי ביום החתונה, וסגירת השובל והאביזרים.</p>
        </div></li>
      </ol>
    </div>
  </section>

  <section class="band band-grey">
    <div class="wrap">
      <div class="band-head">
        <p class="eyebrow">מתוך הסטודיו</p>
        <h2>אילו שמלות תמצאי בסטודיו?</h2>
        <p class="lede">כל דגם ניתן להתאמה: מחשוף, גב, שרוול, אורך ושובל משתנים לפי מבנה הגוף ולפי מה שנוח לך.</p>
      </div>
      <ul class="gowns">
        <li><figure class="gown"><img src="{gown(G['vintage'])}" alt="שמלת כלה בוהו תחרת וינטאג' וטול" loading="lazy" width="760" height="1140"><figcaption>תחרת וינטאג׳ וטול מנוקד</figcaption></figure></li>
        <li><figure class="gown"><img src="{gown(G['heart'])}" alt="שמלת בוהו תחרה וטול עם מחשוף לב" loading="lazy" width="760" height="1140"><figcaption>מחוך לב חצי שקוף וגב פתוח</figcaption></figure></li>
        <li><figure class="gown"><img src="{gown(G['train'])}" alt="שמלת כלה בוהו מתחרה עם שובל ארוך" loading="lazy" width="760" height="1140"><figcaption>מחוך לב ושובל ארוך</figcaption></figure></li>
        <li><figure class="gown"><img src="{gown(G['aline'])}" alt="שמלת כלה בוהו בגזרת A-line עם שסע עמוק" loading="lazy" width="760" height="1140"><figcaption>גזרת A-line עם שסע עמוק</figcaption></figure></li>
      </ul>
    </div>
  </section>

{quotes()}

{faq(P1_FAQ, "לפני שאת מגיעה", "שאלות על הפגישה בסטודיו")}

{cta("השאירי פרטים ונחזור אלייך לתאם, או שלחי הודעה בוואטסאפ, זה הכי מהיר.")}''',
 ld(BIZ) + "\n" + ld(faq_schema(P1_FAQ)))

(BASE / 'hod-hasharon.html').write_text(P1, encoding='utf-8')

# ================= PAGE 2 — a segment page from the catalogue =================
# Every gown named here is a real model in the Wix store, so the page is
# answerable at the fitting rather than a promise the studio cannot keep.

P2_FAQ = [
 ("אפשר להוסיף שרוולים לדגם שאין לו?",
  "כן. השמלה נתפרת מההתחלה לפי המידות שלך, אז שרוול הוא החלטה בעיצוב ולא מגבלה של הדגם. במדידה נעבור יחד על מה מתאים לגזרה שבחרת."),
 ("אילו שרוולים מתאימים לחתונת קיץ?",
  "תחרה וטול קלילים כמעט לא מורגשים גם בחום. שרוול קצר ורך או שרוול שקוף על הזרוע יוצרים את המראה בלי הכובד של בד מלא."),
 ("אפשר לשנות את אורך השרוול?",
  "כן. האורך נקבע במדידה, על הגוף שלך, ולא לפי טבלה. אפשר לקצר, להאריך או לשנות את רוחב הפתח בשולי השרוול."),
 ("איך יודעים איזה שרוול מחמיא לי?",
  "מודדים. זו בדיוק הסיבה שהפגישה הראשונה קיימת: שרוול נראה אחרת לגמרי על גופים שונים, ואי אפשר להחליט על זה מתמונה."),
]

P2 = page(
 "שמלות כלה עם שרוולים · שני ששון",
 "שמלות כלה בוהו עם שרוולים: תחרה שקופה, שרוול רחב או קצר. מעוצבות ונתפרות בסטודיו בהוד השרון לפי המידות שלך.",
 f'''  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <p class="eyebrow">סטודיו בעין חי 7, הוד השרון</p>
        <h1>שמלות כלה <em>עם שרוולים</em></h1>
        <p class="lede">
          השרוול משנה שמלה יותר מכל פרט אחר. הוא קובע כמה היא רומנטית, כמה היא מכוסה
          ואיך היא נראית בתמונות. בסטודיו הוא נקבע במדידה, על הגוף שלך.
        </p>
        <div class="btn-row">
          <a class="btn" href="https://wa.me/{WA}?text=%D7%94%D7%99%D7%99%20%D7%A9%D7%A0%D7%99%2C%20%D7%9E%D7%97%D7%A4%D7%A9%D7%AA%20%D7%A9%D7%9E%D7%9C%D7%94%20%D7%A2%D7%9D%20%D7%A9%D7%A8%D7%95%D7%95%D7%9C%D7%99%D7%9D" target="_blank" rel="noopener">{WA_SVG}לקבוע פגישת מדידה</a>
          <a class="btn btn-secondary" href="#דגמים">לראות דגמים</a>
        </div>
        <dl class="facts">
          <div><dt>עיצוב</dt><dd>במידות שלך</dd></div>
          <div><dt>שרוול</dt><dd>נקבע במדידה</dd></div>
          <div><dt>הסטודיו</dt><dd>הוד השרון</dd></div>
        </dl>
      </div>
      <figure class="hero-figure">
        <img src="{gown(G['vintage'],1000,1500)}" alt="שמלת כלה בוהו עם שרוולים רחבים מתחרת וינטאג'" width="1000" height="1500" fetchpriority="high">
        <figcaption>תחרת וינטאג׳ וטול מנוקד, עם שרוולים רחבים ושקופים.</figcaption>
      </figure>
    </div>
  </section>

  <section class="band band-grey">
    <div class="wrap">
      <div class="band-head">
        <p class="eyebrow">שלושה כיוונים</p>
        <h2>אילו שרוולים אפשר בסטודיו?</h2>
      </div>
      <div class="pillars">
        <article class="pillar">
          <span class="pillar-badge">רחב ושקוף</span>
          <h3>שרוול זורם</h3>
          <p>טול או תחרה שקופה שנופלים מהכתף. נותן תנועה בתמונות ומראה בוהו מובהק, בלי לכסות ממש.</p>
        </article>
        <article class="pillar">
          <span class="pillar-badge">תחרה</span>
          <h3>שרוול תחרה על הזרוע</h3>
          <p>צמוד ועדין, ממשיך את התחרה של המחוך אל הזרוע. הכי רומנטי מהשלושה.</p>
        </article>
        <article class="pillar">
          <span class="pillar-badge">קצר</span>
          <h3>שרוול קצר ורך</h3>
          <p>מכסה את הכתף בלבד. קליל לקיץ ומאפשר מחשוף פתוח בלי להרגיש חשופה.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="band" id="דגמים">
    <div class="wrap">
      <div class="band-head">
        <p class="eyebrow">מתוך הסטודיו</p>
        <h2>דגמים עם שרוולים שאפשר למדוד</h2>
        <p class="lede">אלה דגמים קיימים בסטודיו. כל אחד מהם ניתן להתאמה, וגם דגם בלי שרוולים יכול לקבל אותם.</p>
      </div>
      <ul class="gowns">
        <li><figure class="gown"><img src="{gown(G['vintage'])}" alt="שמלת כלה בוהו תחרת וינטאג' עם שרוולים רחבים" loading="lazy" width="760" height="1140"><figcaption>תחרת וינטאג׳ וטול מנוקד · שרוולים רחבים ושקופים</figcaption></figure></li>
        <li><figure class="gown"><img src="{gown(G['train'])}" alt="שמלת כלה בוהו עם שרוולי תחרה ושובל ארוך" loading="lazy" width="760" height="1140"><figcaption>מחוך לב ושובל ארוך · שרוולי תחרה על הזרוע</figcaption></figure></li>
        <li><figure class="gown"><img src="{gown(G['sleeves'])}" alt="שמלת כלה תחרה רומנטית עם שרוולים קצרים" loading="lazy" width="760" height="1140"><figcaption>תחרה קלילה · שרוולים קצרים וקפלים במותן</figcaption></figure></li>
        <li><div class="gown-more">
          <p class="t">ויש גם בלי.</p>
          <p>אם התאהבת בדגם ללא שרוולים, אפשר להוסיף שרוולים בתפירה.</p>
          <a class="btn btn-secondary" href="#פגישה">לקבוע פגישה</a>
        </div></li>
      </ul>
    </div>
  </section>

{quotes()}

{faq(P2_FAQ, "שאלות על שרוולים", "מה כלות שואלות")}

{cta("ספרי לנו איזה שרוול מדברת אלייך, ונגיד לך בדיוק אילו דגמים כדאי למדוד.")}''',
 ld(BIZ) + "\n" + ld(faq_schema(P2_FAQ)))

(BASE / 'shmalot-im-sharvulim.html').write_text(P2, encoding='utf-8')

print("built:")
for f in ('hod-hasharon.html','shmalot-im-sharvulim.html'):
    print(f"  {f}  {(BASE/f).stat().st_size:,} bytes")
