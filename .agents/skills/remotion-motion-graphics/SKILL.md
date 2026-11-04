---
name: remotion-motion-graphics
description: >-
  End-to-end Arabic-first motion-graphics studio workflow for Google Antigravity
  using Remotion, React, Google AI Studio Emotion-Tagged voiceovers, FFmpeg
  frame-accurate silence detection, reference style analysis, and procedural
  Python sound effects. Supports both Code-First procedural graphics and
  Storyboard/Scenes image-assisted modes (Shorts, Reels, TikTok, YouTube 16:9,
  Square 1:1, or 4:5).
---

# Remotion Motion Graphics Studio Skill (Antigravity Edition)

إعداد وتطوير: **د. محمد رفعت (`nre-edu` / Dr. Mohamed Refat)** — مطوّرة خصيصاً لبيئة **Google Antigravity** بالاستفادة من قواعد ومعمارية `arabic-motion`.

قبل كتابة أي نص عربي أو تحديد مقاس الفيديو، اقرأ مرجع القواعد الإلزامية:
[الطباعة العربية، المقاسات، وقائمة الفحص](./references/arabic-typography-and-formats.md)

---

## 🎭 نمطا التشغيل التلقائيان (Dual-Mode Execution)

تتعرف المهارة تلقائياً على أحد نمطين للإنتاج:

### 1️⃣ النمط الأول: التوليد البرمجي بالكود (Code-First Mode — الافتراضي)
* يُستخدم تلقائياً **إذا لم يضع المستخدم صوراً أو لوحة مشاهد**.
* تقوم المهارة ببرمجة وتوليد جميع العناصر البصرية، الكروت ثلاثية الأبعاد، المخططات، والخلفيات بالكود مباشرة في Remotion كما في مشروع Google NotebookLM.

### 2️⃣ النمط الثاني: المدعوم بالمشاهد والستوري بورد (Storyboard / Scenes Mode)
* يُستخدم تلقائياً **إذا وُجد مجلد `scenes/` أو ملف ستوري بورد (مثل `motion-storyboard.png`)**.
* إذا وُجد ملف ستوري بورد مجمّع (مثل شبكة 4×2)، تشغّل المهارة سكربت التقطيع [slice_storyboard.py](./scripts/slice_storyboard.py) لإنتاج صور المشاهد المستقلة.
* تُعرض المشاهد داخل بطاقات سينمائية ثلاثية الأبعاد (`AnimatedSceneCard`) مع حركة دفع بطيئة (`Ken Burns Push-in`)، اهتزاز طفو خفيف، وتزامن كامل مع توقيت الجملة الصوتية.

---

## Step 0: Upfront Project Choices (اسأل المستخدم أولاً)

عند بدء أي مشروع فيديو جديد، استخدم أداة `ask_question` لسؤال المستخدم عن الخيارات الأساسية (إلا إذا حددها مسبقاً في طلبه):

1. **مقاس ونوع الفيديو (Video Format & Aspect Ratio):**
   * **شورتس / ريلز / تيك توك (`9:16` عمودي — `1080×1920`)** *(الافتراضي)*
   * **فيديو يوتيوب كامل (`16:9` أفقي — `1920×1080`)**
   * **منشور مربع (`1:1` — `1080×1080`)**
   * **منشور خلاصة عمودي (`4:5` — `1080×1350`)**
2. **التوقيع واسم المتحدث (Presenter Signature):**
   * **قاعدة صارمة:** لا تضع اسم أو توقيع **"دكتور محمد رفعت / Dr. Mohamed Refat"** تلقائياً أبداً إلا إذا طلب المستخدم ذلك، وفي حال لم يذكره اسأله أولاً إن كان يرغب في إضافته لهذه الحلقة أم لا.

---

## Step 1: Analyze the Episode Reference (`reference/`)

المرجع في `<episode-dir>/reference/` قد يكون **فيديو** (`MP4`/`MOV`)، أو **صورة/إنفوجراف/تصميم Pinterest** (`PNG`/`JPG`/`WEBP`)، أو **الاثنين معاً**:

1. شغّل سكربت القياس والتحليل الآلي [analyze_ref.py](./scripts/analyze_ref.py):
   ```bash
   python .agents/skills/remotion-motion-graphics/scripts/analyze_ref.py <episode-dir>/reference
   ```
   يستخرج السكربت في `reference/analysis/`:
   - `analysis.json`: الأبعاد، المدة، عدد اللقطات، متوسط ووسيط طول اللقطة، القطعات لكل 10 ثوانٍ، وأبرز 6 ألوان (`palette`) بنسبها المئوية.
   - `opening.jpg` (أول 3 ثوانٍ كل 0.5 ثانية)، `shots.jpg` (منتصف كل لقطة)، و`timeline.jpg` (الفيديو بالكامل كل 0.5–1 ثانية).
2. افحص لوحات اللقطات بصرياً عبر `read_file` ووثّق بطاقة الأسلوب في `<episode-dir>/reference/STYLE_GUIDE.md`.
3. **قاعدة الأصالة:** يُؤخذ من المرجع **الأسلوب والإيقاع وروح التصميم فقط**؛ لا تنسخ صوره أو شعاراته أو موسيقاه.

---

## Step 2: Author the Script with Google AI Studio Emotion Tags

1. **أسلوب الخطاف السريع (Hook-First):**
   * ابدأ فوراً في أول 0–3 ثوانٍ بجملة أو سؤال يثير الفضول بدون أي مقدمات ترحيبية بطيئة.
   * إذا طلب المستخدم تضمين اسمه، اكتبه نصاً صريحاً **"دكتور محمد رفعت"** في اسكربت الصوت لتجنب قراءة اختصار `د.` بشكل خاطئ.
2. **تاجات المشاعر الخاصة بـ Google AI Studio (إلزامي):**
   * أدرج تاجات المشاعر الصوتية داخل الاسكربت وفق صيغة **Google AI Studio**:
     ```text
     Emotion Tags:<gasp> That's a great idea! <laugh> (Type '<' for tags)
     ```
   * التاجات المعتمدة وتأثيرها الحركي في Remotion:
     * `<curious>` — للهوك التساؤلي المشوق (دخول `blur -> sharp`).
     * `<pause>` / `<short pause>` — وقفة قصيرة لتعليق الانتباه والفصل بين مرحلتين.
     * `<enthusiastic>` / `<excited>` — حماس وطاقة عالية (ارتداد `spring` سريع + `pop`).
     * `<wonder>` — نبرة إعجاب وإبهار عند شرح قدرات الذكاء الاصطناعي.
     * `<chuckle>` / `<laugh>` — ابتسامة صوتية طبيعية لكسر الجمود.
     * `<confident>` / `<smile>` — نبرة ختامية واثقة ومقنعة في الـ Punchline والـ CTA.
     * `<gasp>` / `<sigh>` / `<whisper>` — حسب السياق الدرامي.
3. اعرض الاسكربت جاهزاً للنسخ ليقوم المستخدم بتوليد الصوت من **Google AI Studio** (`24kHz WAV`) ووضعه في `<episode-dir>/public/voice.wav`.

---

## Step 3: Detect Speech Timings & Map Frames (`30fps`)

1. انسخ ملف الصوت المولّد إلى `<episode-dir>/public/voice.wav`.
2. شغّل سكربت تحليل الصمت [analyze_voice_timings.py](./scripts/analyze_voice_timings.py):
   ```bash
   python .agents/skills/remotion-motion-graphics/scripts/analyze_voice_timings.py <episode-dir>/public/voice.wav
   ```
3. اقرأ ملف الصوت عبر `read_file` لمطابقة كل جملة منطوقة مع إطار بدايتها ونهايتها بدقة (`Frames @ 30fps`).

---

## Step 4: Handle Scene Assets & Procedural SFX

1. **فحص المشاهد والستوري بورد (Scene Assets):**
   * إذا وُجد ملف ستوري بورد مجمّع (مثل `motion-storyboard.png` بشبكة 4×2)، قم بتقطيعه:
     ```bash
     python .agents/skills/remotion-motion-graphics/scripts/slice_storyboard.py <episode-dir>/motion-storyboard.png <episode-dir>/public/scenes --cols 4 --rows 2
     ```
   * إذا وُجد مجلد `scenes/` جاهز، انسخه إلى `<episode-dir>/public/scenes/`.
   * إذا لم توجد صور مشاهد، يتم تفعيل **النمط التوليدي بالكود (Code-First)** مباشرة.
2. **توليد المؤثرات الصوتية (`public/sfx.wav`):**
   * شغّل سكربت [generate_sfx.py](./scripts/generate_sfx.py) لتوليد مسار `sfx.wav` متزامناً مع فواصل المشاهد:
     * خلفية موسيقية تقنية دافئة ومنخفضة (`Ambient Tech Pad`).
     * مؤثرات انتقال (`whoosh`) عند بداية كل مشهد، ونقرات (`pop`) عند ظهور البطاقات، وضربة الختام (`impact`).

---

## Step 5: Build, Verify Arabic Typography & Render in Remotion (`src/Root.tsx`)

1. **تطبيق قواعد الطباعة العربية الإلزامية (من [المرجع](./references/arabic-typography-and-formats.md)):**
   * **الكلمة أو السطر أصغر وحدة متحركة:** يُمنع تحريك الحروف العربية حرفاً بحرف أو إضافة `letterSpacing` للنص العربي.
   * اتجاه الحاويات العربية `dir="rtl"` مع حماية النقاط والذيول والالتزام بالمنطقة الآمنة (`Safe Zone`).
   * عدم إظهار أي تاج صوتي (`<...>` أو `[...]`) على الشاشة إطلاقاً.
2. **البناء والتصدير (`Render`):**
   * في حال كان المشروع على قرص سحابي افتراضي (مثل Google Drive `J:\`) يمنع فك حزم `node_modules`، قم ببناء وتصدير الفيديو داخل مجلد مؤقت على القرص المحلي `C:\` ثم انسخ الفيديو النهائي `.mp4` ولوحة المعاينة `contact-sheet-preview.jpg` إلى مجلد الحلقة.
3. **الفحص الداخلي قبل التسليم (QA Check):**
   * استخرج لوحة معاينة شاملة للمشاهد وافحصها عبر `read_file` للتأكد من سلامة المشاهد، عدم وجود إطارات فارغة، ومطابقة الهوية البصرية للمرجع.
