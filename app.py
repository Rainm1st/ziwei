# -*- coding: utf-8 -*-
from flask import Flask, request, render_template_string
from datetime import datetime
import os

app = Flask(__name__)

PALACES = [
    "命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫",
    "迁移宫", "交友宫", "官禄宫", "田宅宫", "福德宫", "父母宫"
]

STAR_TRAITS = {
    "紫微": "有领导感，适合站在较高视角统筹全局，但也容易对自己要求很高。",
    "天机": "思维灵活，善于策划与变通，适合需要判断力和创意的领域。",
    "太阳": "外向坦荡，重视责任感，适合主动表达、影响他人和承担事务。",
    "武曲": "执行力强，重视结果与效率，对金钱、资源和实际成果较敏感。",
    "天同": "性情温和，重视舒适感和人情味，适合稳定、长期、有温度的环境。",
    "廉贞": "有原则、有欲望感，也有管理和社交能力，适合竞争性较强的场景。",
    "天府": "稳重务实，重视安全感和积累，适合资源管理、财务、经营类方向。",
    "太阴": "细腻敏感，重视内在感受、家庭和审美，适合细致、策划、照顾型角色。",
    "贪狼": "兴趣广泛，社交和表现欲较强，适合多元发展、娱乐、销售、内容行业。",
    "巨门": "表达和分析能力强，适合研究、咨询、谈判，但要注意过度怀疑。",
    "天相": "重视公平、秩序和协调，适合组织管理、服务、行政、顾问型工作。",
    "天梁": "成熟稳重，有照顾他人的倾向，适合教育、咨询、管理和公益类方向。",
    "七杀": "行动果断，有冲劲，适合开创、竞争、突破型环境，但要注意节奏。",
    "破军": "喜欢改变，不怕打破旧模式，适合创新、转型、创业和新领域探索。",
}

PALACE_MEANINGS = {
    "命宫": "代表性格底色、天赋、人生格局与自我认同。",
    "兄弟宫": "代表手足、同辈、朋友支持与合作关系。",
    "夫妻宫": "代表感情模式、伴侣关系与亲密关系中的需求。",
    "子女宫": "代表子女缘分、创造力、表达欲和下属缘。",
    "财帛宫": "代表赚钱方式、理财观念、资源敏感度。",
    "疾厄宫": "代表身体状态、压力来源和健康倾向。",
    "迁移宫": "代表外出发展、变化机会、异地缘分与外部环境。",
    "交友宫": "代表朋友、人脉、合作伙伴和团队关系。",
    "官禄宫": "代表事业方向、职业风格、社会角色和成就感。",
    "田宅宫": "代表家庭、房产、居住环境和长期资产。",
    "福德宫": "代表精神状态、兴趣、享受能力和内在满足。",
    "父母宫": "代表长辈、上司、原生家庭和被支持的方式。",
}

def calculate_palace_index(hour, month):
    if 23 <= hour or hour < 1:
        tb = 0
    elif 1 <= hour < 3:
        tb = 1
    elif 3 <= hour < 5:
        tb = 2
    elif 5 <= hour < 7:
        tb = 3
    elif 7 <= hour < 9:
        tb = 4
    elif 9 <= hour < 11:
        tb = 5
    elif 11 <= hour < 13:
        tb = 6
    elif 13 <= hour < 15:
        tb = 7
    elif 15 <= hour < 17:
        tb = 8
    elif 17 <= hour < 19:
        tb = 9
    elif 19 <= hour < 21:
        tb = 10
    else:
        tb = 11
    ming_index = (month - tb + 2) % 12
    return [(ming_index + i) % 12 for i in range(12)]

def distribute_stars(palace_indices, gender):
    palaces_stars = {n: {"main_stars": [], "auxiliary_stars": []} for n in PALACES}
    ming_index = palace_indices[0]

    positions = {
        "紫微": ming_index,
        "天机": (ming_index + 1) % 12,
        "太阳": (ming_index + 2) % 12,
        "武曲": (ming_index + 3) % 12,
        "天同": (ming_index + 4) % 12,
        "廉贞": (ming_index + 5) % 12,
        "天府": (4 - ming_index) % 12,
        "太阴": (5 - ming_index) % 12,
        "贪狼": (6 - ming_index) % 12,
        "巨门": (7 - ming_index) % 12,
        "天相": (8 - ming_index) % 12,
        "天梁": (9 - ming_index) % 12,
        "七杀": (10 - ming_index) % 12,
        "破军": (11 - ming_index) % 12,
    }

    for star, pos in positions.items():
        palaces_stars[PALACES[pos]]["main_stars"].append(star)

    if gender == "男":
        palaces_stars["财帛宫"]["auxiliary_stars"].append("左辅")
        palaces_stars["官禄宫"]["auxiliary_stars"].append("右弼")
    else:
        palaces_stars["官禄宫"]["auxiliary_stars"].append("左辅")
        palaces_stars["财帛宫"]["auxiliary_stars"].append("右弼")

    palaces_stars["夫妻宫"]["auxiliary_stars"].append("文昌")
    palaces_stars["福德宫"]["auxiliary_stars"].append("文曲")
    return palaces_stars

def make_palace_text(palace, main_stars, auxiliary_stars):
    main_text = "、".join(main_stars) if main_stars else "无明显主星"
    aux_text = "；辅星：" + "、".join(auxiliary_stars) if auxiliary_stars else ""
    traits = [STAR_TRAITS.get(s, "") for s in main_stars if s in STAR_TRAITS]
    trait_text = " ".join(traits) if traits else "这一宫位更需要结合三方四正和流年变化来观察。"
    return f"{palace}主星为：{main_text}{aux_text}。{PALACE_MEANINGS[palace]} {trait_text}"

def generate_chart(name, birth_date, birth_time, gender, address):
    y, m, d = [int(x) for x in birth_date.split("-")]
    hour = int(birth_time.split(":")[0])
    stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    year_stem = stems[(y - 4) % 10]
    palace_indices = calculate_palace_index(hour, m)
    palaces_stars = distribute_stars(palace_indices, gender)

    palaces = {}
    for i, palace in enumerate(PALACES):
        stars = palaces_stars[palace]
        palaces[palace] = {
            "position": i + 1,
            "main_stars": stars["main_stars"],
            "auxiliary_stars": stars["auxiliary_stars"],
            "meaning": PALACE_MEANINGS[palace],
            "interpretation": make_palace_text(palace, stars["main_stars"], stars["auxiliary_stars"]),
        }

    ming_stars = palaces["命宫"]["main_stars"]
    star_text = "、".join(ming_stars) if ming_stars else "无明显主星"
    traits = [STAR_TRAITS.get(s, "") for s in ming_stars if s in STAR_TRAITS]
    trait_text = " ".join(traits) if traits else "你的命宫结构比较含蓄，适合从事业宫、财帛宫和迁移宫一起判断。"

    return {
        "name": name,
        "birth_info": {
            "solar_date": birth_date,
            "birth_time": birth_time,
            "gender": gender,
            "address": address,
            "year_stem": year_stem,
        },
        "palaces": palaces,
        "overall": {
            "summary": f"{name or '你'}的命宫主星为 {star_text}。{trait_text}",
            "career": palaces["官禄宫"]["interpretation"],
            "wealth": palaces["财帛宫"]["interpretation"],
            "relationship": palaces["夫妻宫"]["interpretation"],
            "advice": "这份解读适合当作自我观察的参考，不建议把它当成唯一决策依据。更好的用法是：看见自己的倾向，然后主动调整选择、节奏和沟通方式。",
        },
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

HTML = """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>紫薇斗数 AI 解读</title>
  <style>
    :root {
      --bg: #120d1f;
      --card: rgba(255,255,255,.08);
      --card2: rgba(255,255,255,.12);
      --text: #f7f2ff;
      --muted: #cbbfe3;
      --gold: #f4c76b;
      --line: rgba(255,255,255,.14);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 20% 10%, rgba(133,78,255,.35), transparent 30%),
        radial-gradient(circle at 80% 0%, rgba(244,199,107,.18), transparent 25%),
        linear-gradient(135deg, #120d1f, #241634 55%, #100b18);
      min-height: 100vh;
    }
    .wrap { max-width: 1120px; margin: 0 auto; padding: 32px 18px 64px; }
    .hero { padding: 36px 0 24px; }
    .badge { display:inline-flex; gap:8px; align-items:center; padding:8px 12px; border:1px solid var(--line); border-radius:999px; color:var(--gold); background:rgba(255,255,255,.06); font-size:14px; }
    h1 { font-size: clamp(34px, 7vw, 68px); line-height: 1.04; margin: 18px 0 12px; letter-spacing: -1px; }
    .lead { color: var(--muted); font-size: 18px; line-height: 1.8; max-width: 760px; }
    .grid { display: grid; grid-template-columns: 1fr; gap: 18px; }
    @media (min-width: 900px) { .grid { grid-template-columns: 420px 1fr; } }
    .card {
      border: 1px solid var(--line);
      border-radius: 28px;
      background: var(--card);
      backdrop-filter: blur(18px);
      box-shadow: 0 24px 80px rgba(0,0,0,.28);
      padding: 22px;
    }
    label { display:block; color:var(--muted); font-size:14px; margin: 14px 0 8px; }
    input, select {
      width: 100%;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.08);
      color: var(--text);
      border-radius: 16px;
      padding: 14px 14px;
      outline: none;
      font-size: 15px;
    }
    select option { color: #111; }
    button {
      margin-top: 20px;
      width: 100%;
      border: 0;
      border-radius: 18px;
      padding: 15px 18px;
      font-size: 16px;
      font-weight: 700;
      color: #261305;
      background: linear-gradient(135deg, #ffe6a3, #f4c76b);
      cursor: pointer;
      box-shadow: 0 12px 30px rgba(244,199,107,.25);
    }
    .hint { color: var(--muted); font-size: 13px; line-height: 1.7; margin-top: 12px; }
    .section-title { font-size: 22px; margin: 0 0 14px; }
    .result-head { display:flex; flex-wrap:wrap; gap:10px; margin-bottom: 16px; }
    .pill { padding: 8px 11px; border-radius: 999px; background: rgba(244,199,107,.14); color: #ffe6a3; font-size:13px; border:1px solid rgba(244,199,107,.22); }
    .bigtext { line-height: 1.85; color: #f4edf9; font-size: 16px; }
    .palaces { display:grid; grid-template-columns:1fr; gap:12px; margin-top: 16px; }
    @media (min-width: 700px) { .palaces { grid-template-columns: repeat(2, 1fr); } }
    .palace { background: var(--card2); border: 1px solid var(--line); border-radius: 20px; padding: 16px; }
    .palace h3 { margin:0 0 8px; color:var(--gold); font-size:17px; }
    .palace p { margin:0; color:var(--muted); line-height:1.72; font-size:14px; }
    .empty { min-height: 360px; display:grid; place-items:center; text-align:center; color: var(--muted); }
    .notice { margin-top: 18px; padding: 14px 16px; border-radius: 18px; border:1px solid rgba(244,199,107,.22); background: rgba(244,199,107,.1); color:#ffe6a3; line-height:1.7; font-size:14px; }
    footer { color: var(--muted); text-align:center; margin-top: 32px; font-size:13px; }
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <span class="badge">✦ Zi Wei Dou Shu Reading</span>
      <h1>紫薇斗数<br>AI 命盘解读</h1>
      <p class="lead">输入出生信息，即可生成一份基础命盘与十二宫解读。适合用于性格观察、事业方向、感情模式与自我探索。</p>
    </section>

    <main class="grid">
      <form class="card" method="post">
        <h2 class="section-title">填写出生信息</h2>

        <label>姓名 / 昵称</label>
        <input name="name" placeholder="例如：小林" value="{{ form.name or '' }}">

        <label>出生日期（公历）</label>
        <input name="birth_date" type="date" required value="{{ form.birth_date or '' }}">

        <label>出生时间</label>
        <input name="birth_time" type="time" required value="{{ form.birth_time or '' }}">

        <label>性别</label>
        <select name="gender" required>
          <option value="男" {% if form.gender == '男' %}selected{% endif %}>男</option>
          <option value="女" {% if form.gender == '女' %}selected{% endif %}>女</option>
        </select>

        <label>出生地</label>
        <input name="address" placeholder="例如：北京 / 上海 / 新加坡" value="{{ form.address or '' }}">

        <button type="submit">生成命盘解读</button>
        <p class="hint">说明：当前版本为演示型排盘网站，适合先上线验证产品形态。正式商用前建议升级完整排盘算法。</p>
      </form>

      <section class="card">
        {% if chart %}
          <div class="result-head">
            <span class="pill">{{ chart.name or '匿名用户' }}</span>
            <span class="pill">{{ chart.birth_info.solar_date }} {{ chart.birth_info.birth_time }}</span>
            <span class="pill">{{ chart.birth_info.gender }}</span>
            <span class="pill">{{ chart.birth_info.year_stem }}年生</span>
          </div>

          <h2 class="section-title">总体解读</h2>
          <p class="bigtext">{{ chart.overall.summary }}</p>

          <div class="notice">
            <strong>事业：</strong>{{ chart.overall.career }}<br>
            <strong>财运：</strong>{{ chart.overall.wealth }}<br>
            <strong>感情：</strong>{{ chart.overall.relationship }}<br>
            <strong>建议：</strong>{{ chart.overall.advice }}
          </div>

          <h2 class="section-title" style="margin-top:22px;">十二宫位</h2>
          <div class="palaces">
            {% for palace, item in chart.palaces.items() %}
              <div class="palace">
                <h3>{{ palace }}</h3>
                <p>{{ item.interpretation }}</p>
              </div>
            {% endfor %}
          </div>
        {% else %}
          <div class="empty">
            <div>
              <h2>你的命盘会显示在这里</h2>
              <p>填写左侧信息后，系统会生成基础命盘、总体解读和十二宫分析。</p>
            </div>
          </div>
        {% endif %}
      </section>
    </main>

    <footer>
      本工具仅供娱乐与自我探索参考，不构成任何人生、医疗、法律或投资决策建议。
    </footer>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    chart = None
    form = {}
    if request.method == "POST":
        form = {
            "name": request.form.get("name", "").strip(),
            "birth_date": request.form.get("birth_date", "").strip(),
            "birth_time": request.form.get("birth_time", "").strip(),
            "gender": request.form.get("gender", "男").strip(),
            "address": request.form.get("address", "").strip(),
        }
        try:
            chart = generate_chart(
                form["name"], form["birth_date"], form["birth_time"], form["gender"], form["address"]
            )
        except Exception as exc:
            chart = {
                "name": form.get("name", ""),
                "birth_info": {
                    "solar_date": form.get("birth_date", ""),
                    "birth_time": form.get("birth_time", ""),
                    "gender": form.get("gender", ""),
                    "address": form.get("address", ""),
                    "year_stem": "",
                },
                "palaces": {},
                "overall": {
                    "summary": f"生成失败：{exc}",
                    "career": "",
                    "wealth": "",
                    "relationship": "",
                    "advice": "请检查日期、时间和性别是否填写完整。",
                },
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

    return render_template_string(HTML, chart=chart, form=form)

@app.route("/api/chart", methods=["POST"])
def api_chart():
    data = request.get_json(force=True, silent=True) or {}
    required = ["birth_date", "birth_time", "gender"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        return {"error": f"Missing fields: {', '.join(missing)}"}, 400

    return generate_chart(
        data.get("name", ""),
        data["birth_date"],
        data["birth_time"],
        data["gender"],
        data.get("address", ""),
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
