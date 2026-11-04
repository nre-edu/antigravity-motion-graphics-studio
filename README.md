# 🎬 استوديو ومهارة صناعة الموشن جرافيك (Antigravity + Remotion Studio)

مهارة ومنهجية عمل متكاملة ومُهيّأة لبيئة **Google Antigravity** لصناعة فيديوهات الموشن جرافيك العربية برمجياً باستخدام **Remotion & React**، مع توليد التعليق الصوتي عبر **Google AI Studio** ومزامنة الصوت والحركة بالمللي ثانية، بالاستفادة من معمارية وقواعد الطباعة العربية في مشروع [`arabic-motion`](https://github.com/nre-edu/arabic-motion).

---

## 🚀 دليل الاستخدام السريع للمستخدم (How to Use)

إذا كنت تستخدم **Google Antigravity** أو تعمل على هذا المستودع، فإن استخدام المهارة بسيط وتفاعلي للغاية:

### 1. ما تكتبه في المحادثة (الطلب المبدئي)
يكفي أن تطلب من المساعد البدء في حلقة جديدة وتحدد الفكرة:
> **«عايز أعمل فيديو موشن جرافيك جديد عن [موضوع الفيديو] وده المرجع في مجلد reference»**

### 2. ما تجهزه أنت فقط (User Inputs)
1. **المرجع:** ضع الفيديو المرجعي أو الصور/الإنفوجراف داخل مجلد `reference/`.
2. **الصوت:** بعد أن يصيغ لك المساعد الاسكربت مدمجاً بتاجات المشاعر، انسخه إلى **Google AI Studio**، وقم بتوليد الصوت ثم ضعه في `public/voice.wav`.

### 3. ما يقوم به Antigravity تلقائياً
1. **يسألك أولاً:** عن مقاس الفيديو المطلوب (`9:16` ريل/شورت، `16:9` أفقي، `1:1` مربع، أو `4:5`) وعما إذا كنت ترغب في إضافة اسمك/توقيعك.
2. **يحلل المرجع:** يقيس الألوان، طول اللقطات، وسرعة الحركة.
3. **يحلل الصوت:** يستخرج بداية ونهاية كل جملة بالمللي ثانية ويحوّلها إلى أرقام إطارات (`Frames @ 30fps`).
4. **يولّد المؤثرات الصوتية (`sfx.wav`):** موسيقى خلفية هادئة + مؤثرات Whoosh + نقرات Pop + ضربة الختام.
5. **يبرمج ويصدّر الفيديو:** يكتب المشاهد بكود Remotion مع تطبيق قواعد الطباعة العربية الصارمة ويصدّر لك ملف الفيديو النهائي `.mp4`.

---

## 🧠 محتويات مهارة Antigravity (`remotion-motion-graphics`)

تقع المهارة داخل المسار القياسي لاكتشاف المهارات في Antigravity:
[`.agents/skills/remotion-motion-graphics/SKILL.md`](./.agents/skills/remotion-motion-graphics/SKILL.md)

وتضم الوحدات التالية:
* **دليل التشغيل الآلي ([`SKILL.md`](./.agents/skills/remotion-motion-graphics/SKILL.md)):** خطوات سؤال المستخدم عن المقاس والتوقيع، تحليل المرجع، كتابة الاسكربت بتاجات المشاعر، وبناء مشاهد Remotion.
* **مرجع الطباعة العربية والمقاسات ([`arabic-typography-and-formats.md`](./.agents/skills/remotion-motion-graphics/references/arabic-typography-and-formats.md)):** قواعد اتصال الحروف العربية، المناطق الآمنة (`Safe Zones`) لكل منصة، الخطوط الحرة (`OFL`)، وربط تاجات المشاعر بطابع الحركة.
* **محلل المرجع الآلي ([`analyze_ref.py`](./.agents/skills/remotion-motion-graphics/scripts/analyze_ref.py)):** يقيس طول اللقطات، القطعات لكل 10 ثوانٍ، يستخرج أبرز 6 ألوان (`palette`) بنسبها، ويولّد لوحات `opening.jpg` و`shots.jpg` و`timeline.jpg`.
* **محلل توقيتات الصوت ([`analyze_voice_timings.py`](./.agents/skills/remotion-motion-graphics/scripts/analyze_voice_timings.py)):** يستخرج توقيت كل جملة بالثواني والإطارات (`Frames @ 30fps`) عبر `FFmpeg Silence Detection`.
* **مولّد المؤثرات الصوتية ([`generate_sfx.py`](./.agents/skills/remotion-motion-graphics/scripts/generate_sfx.py)):** يولّد برمجياً ملف `sfx.wav` (موسيقى خلفية تقنية هادئة + مؤثرات انتقال + نقرات + عدّاد + ارتطام الهدف).
* **قالب مشروع Remotion الجاهز ([`templates/remotion-starter/`](./.agents/skills/remotion-motion-graphics/templates/remotion-starter)):** يضم المكونات البصرية الجاهزة (`Sphere3D`, `SelectionBox`, `SparkleStar`, `GridBackground`, `FORMATS`) في [`MotionPrimitives.tsx`](./.agents/skills/remotion-motion-graphics/templates/remotion-starter/src/components/MotionPrimitives.tsx).

---

## 📐 خيارات مقاسات الموشن جرافيك المدعومة (Supported Video Formats)

عند بدء أي فيديو جديد، تخيّر المهارة المستخدم لاختيار المقاس المناسب للمنصة المستهدفة مع إعادة تخطيط العناصر والمناطق الآمنة تلقائياً:

| نوع الفيديو / المنصة | النسبة | الأبعاد (`width × height`) | المنطقة الآمنة (Safe Zone) |
| :--- | :--- | :--- | :--- |
| **شورتس / ريلز / تيك توك (Shorts / Reels / TikTok)** | `9:16` (عمودي) | `1080 × 1920` (30fps) | `220px` أعلى و`360px` أسفل لواجهات التطبيقات |
| **فيديو يوتيوب كامل (YouTube Horizontal)** | `16:9` (أفقي) | `1920 × 1080` (30fps) | هامش `120px` من جميع الحواف وتخطيط عرضي |
| **منشور مربع (Square Post - Instagram / LinkedIn)** | `1:1` (مربع) | `1080 × 1080` (30fps) | تخطيط مركزي متوازن بسطرين كحد أقصى للعنوان |
| **منشور خلاصة عمودي (Portrait Feed Post)** | `4:5` (عمودي) | `1080 × 1350` (30fps) | هامش علوي وسفلي `140px` |

---

## 🔄 منهجية الإنتاج المعتمدة (Standard Production Workflow)

بما أن **كل فكرة فيديو لها مرجع خاص بها** (فيديو أو إنفوجراف أو صورة Pinterest) يتناسب مع طبيعتها، تتبع المهارة الخطوات التالية في كل مشروع:

### 0️⃣ تحديد المقاس وخيار التوقيع (`Upfront Options`)
* سؤال المستخدم عن **مقاس الفيديو** (`9:16` شورت/ريل، `16:9` فيديو أفقي، `1:1` مربع، أو `4:5`).
* **قاعدة اسم المتحدث / التوقيع:** **لا يتم وضع اسم أو توقيع "دكتور محمد رفعت" في الاسكربت أو الفيديو إلا إذا طلب المستخدم ذلك صراحةً**، وفي حال لم يطلب يتم سؤاله أولاً قبل إضافته (وعند إضافته يُكتب نصاً صريحاً "دكتور محمد رفعت" في اسكربت الصوت لتجنب قراءة اختصار `د.` بشكل خاطئ).

### 1️⃣ تحليل المرجع الخاص بالحلقة (`reference/`)
* تشغيل `analyze_ref.py` على مجلد `reference/` لاستخراج لوحات اللقطات (`opening.jpg`, `shots.jpg`, `timeline.jpg`) وملف القياسات اللونية والإيقاعية (`analysis.json`)، وتوثيق الهوية البصرية في `STYLE_GUIDE.md`.

### 2️⃣ كتابة الاسكربت وتوليد الصوت عبر Google AI Studio 🎙️
* صياغة الاسكربت بأسلوب **الخطاف السريع (Hook-First)** بدون مقدمات تقليدية بطيئة.
* **قاعدة أساسية ثابتة:** إضافة **تاجات المشاعر الخاصة بـ Google AI Studio** داخل الاسكربت بصيغة:
  `Emotion Tags:<gasp> That's a great idea! <laugh> (Type '<' for tags)`
* **أهم التاجات المستخدمة وأثرها الحركي:**
  * `<curious>` / `<wonder>` (فضول وإعجاب ← دخول `blur` إلى حاد)
  * `<pause>` / `<short pause>` (وقفة درامية ← فصل بين مرحلتين داخل المشهد)
  * `<enthusiastic>` / `<excited>` / `<gasp>` (حماس ومفاجأة ← ارتداد `spring` سريع وتكبير `pop`)
  * `<chuckle>` / `<laugh>` (ابتسامة صوتية طبيعية لكسر الجمود)
  * `<confident>` / `<smile>` (نبرة ختامية واثقة ومقنعة في الـ CTA ← مؤثر `impact`)
* توليد الملف الصوتي من **Google AI Studio** (`24kHz WAV`) ووضعه في `public/voice.wav`.

### 3️⃣ تحليل التوقيتات الصوتية بالمللي ثانية (`FFmpeg Silence Detection`) ⏱️
* فحص ملف `voice.wav` عبر سكربت `analyze_voice_timings.py` لاستخراج التوقيت الدقيق لبداية ونهاية كل جملة وكلمة مفتاحية، وتحويلها إلى أرقام إطارات (`Frames @ 30fps`).

### 4️⃣ توليد المؤثرات الصوتية والخلفية الموسيقية برمجياً (`Procedural SFX`) 🔊
* تشغيل سكربت `generate_sfx.py` لتوليد ملف `public/sfx.wav` متزامن مع إطارات الفيديو (خلفية موسيقية هادئة + `Whooshes` + `UI Pops` + `Ticks` + `Typing Clicks` + `Impact Hits`).

### 5️⃣ برمجة المشاهد وفحص الطباعة العربية وتصدير الفيديو (`Remotion Render`) 🚀
* الالتزام بقواعد الطباعة العربية (الكلمة أصغر وحدة متحركة، منع `letterSpacing` على النص العربي، اتجاه `dir="rtl"`، وحماية النقاط والذيول داخل المنطقة الآمنة).
* استخراج لوحة معاينة (`contact-sheet-preview.jpg`) للتحقق من الجودة البصرية، ثم تصدير الفيديو النهائي بصيغة `MP4`.

---

## 📂 هيكل المستودع (Repository Structure)

```text
antigravity-motion-graphics-studio/
├── .agents/
│   └── skills/
│       └── remotion-motion-graphics/          # مهارة Antigravity المتكاملة
│           ├── SKILL.md                       # ملف تعليمات المهارة الرئيسي
│           ├── references/
│           │   └── arabic-typography-and-formats.md
│           ├── scripts/
│           │   ├── analyze_ref.py
│           │   ├── analyze_voice_timings.py
│           │   └── generate_sfx.py
│           └── templates/
│               └── remotion-starter/          # قالب مشروع Remotion الجاهز
│                   ├── package.json
│                   ├── tsconfig.json
│                   └── src/
│                       ├── index.ts
│                       ├── Root.tsx
│                       └── components/
│                           └── MotionPrimitives.tsx
├── README.md                                  # التوثيق الشامل للمهارة والاستوديو
└── .gitignore
```

---

## 👨‍💻 إنتاج وتطوير (Produced & Developed By)

تم تصميم وإنتاج وتطوير هذا المشروع ومنهجية العمل بواسطة:
**د. محمد رفعت | Dr. Mohamed Refat** ([@nre-edu](https://github.com/nre-edu))
