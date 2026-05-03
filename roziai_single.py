"""
RoziAI - Complete Single File Application
==========================================
SETUP (one time only):
1. pip install streamlit groq python-dotenv

2. Replace these two lines below with your real Groq API key:
   GROQ_API_KEY = "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"

3. In VS Code terminal run:
   streamlit run roziai.py
"""

# ── PUT YOUR GROQ API KEY HERE ─────────────────────────────────────────────
GROQ_API_KEY = "your_groq_key_here"
# ──────────────────────────────────────────────────────────────────────────

import streamlit as st
import json
import re
import os
import sqlite3
import urllib.parse
from datetime import datetime
from groq import Groq

# ── CLIENTS ───────────────────────────────────────────────────────────────
groq_client = Groq(api_key=GROQ_API_KEY)

# ── PAGE CONFIG ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RoziAI — Har Haath Ko Kaam",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #080b12 !important;
    color: #e2e8f0 !important;
    font-family: 'Sora', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

/* HERO */
.rozi-hero {
    background: linear-gradient(135deg, #0d1117 0%, #0f1923 60%, #0d1117 100%);
    border-bottom: 1px solid #1a2535;
    padding: 2.5rem 2.5rem 2rem;
    position: relative;
    overflow: hidden;
}
.rozi-hero::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-logo {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -2px;
    color: #f1f5f9;
    line-height: 1;
}
.hero-logo span { color: #10b981; }
.hero-tagline {
    font-size: 0.8rem;
    color: #64748b;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.35rem;
}
.hero-urdu {
    font-family: 'Noto Nastaliq Urdu', serif;
    font-size: 1.15rem;
    color: #10b981;
    direction: rtl;
    margin-top: 0.25rem;
}
.stat-row { display: flex; gap: 0.75rem; margin-top: 1.5rem; flex-wrap: wrap; }
.stat-pill {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.18);
    border-radius: 100px;
    padding: 0.3rem 0.9rem;
    font-size: 0.75rem;
    color: #10b981;
    font-weight: 600;
    letter-spacing: 0.04em;
}

/* CARDS */
.glass-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid #1a2535;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.glass-card:hover { border-color: rgba(16,185,129,0.25); }

/* WORKER CARD */
.worker-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid #1a2535;
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: flex-start;
    gap: 1.25rem;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
}
.worker-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #10b981, #6366f1);
    border-radius: 3px 0 0 3px;
}
.worker-card:hover {
    border-color: rgba(16,185,129,0.3);
    transform: translateY(-1px);
    box-shadow: 0 8px 32px rgba(16,185,129,0.07);
}
.worker-avatar {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #10b981 0%, #6366f1 100%);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
}
.worker-name { font-size: 1rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.2rem; }
.worker-meta { font-size: 0.78rem; color: #7a8899; margin-bottom: 0.45rem; }
.worker-meta strong { color: #a0aec0; }
.worker-badges { display: flex; gap: 0.45rem; flex-wrap: wrap; }
.badge {
    font-size: 0.7rem; font-weight: 600;
    padding: 0.18rem 0.6rem; border-radius: 100px; letter-spacing: 0.03em;
}
.badge-green { background: rgba(16,185,129,0.1); color: #10b981; border: 1px solid rgba(16,185,129,0.22); }
.badge-blue  { background: rgba(99,102,241,0.1); color: #818cf8; border: 1px solid rgba(99,102,241,0.22); }
.badge-amber { background: rgba(245,158,11,0.1); color: #fbbf24; border: 1px solid rgba(245,158,11,0.22); }
.badge-red   { background: rgba(239,68,68,0.08); color: #f87171; border: 1px solid rgba(239,68,68,0.18); }
.worker-summary { font-size: 0.78rem; color: #64748b; margin-top: 0.4rem; line-height: 1.55; }
.worker-rate {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem; font-weight: 600; color: #10b981;
    margin-left: auto; text-align: right; white-space: nowrap; padding-left: 1rem;
}
.worker-rate small { display: block; font-size: 0.65rem; color: #4a5568; font-weight: 400; margin-top: 0.1rem; }

/* TRANSCRIPT */
.transcript-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid #1e2d3d;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-family: 'Noto Nastaliq Urdu', serif;
    font-size: 1.1rem;
    direction: rtl;
    color: #c0ccd8;
    line-height: 1.85;
    min-height: 80px;
}

/* BANNERS */
.banner-success {
    background: rgba(16,185,129,0.07);
    border: 1px solid rgba(16,185,129,0.22);
    border-radius: 12px;
    padding: 0.8rem 1.1rem;
    font-size: 0.83rem;
    color: #10b981;
    margin: 0.75rem 0;
}
.banner-info {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 12px;
    padding: 0.8rem 1.1rem;
    font-size: 0.83rem;
    color: #818cf8;
    margin: 0.75rem 0;
}

/* WHATSAPP */
.wa-btn {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: #25D366; color: #fff !important;
    text-decoration: none !important;
    font-family: 'Sora', sans-serif;
    font-size: 0.76rem; font-weight: 700;
    padding: 0.38rem 0.85rem; border-radius: 100px;
    letter-spacing: 0.04em; transition: all 0.2s;
}
.wa-btn:hover { background: #1da851; transform: translateY(-1px); box-shadow: 0 4px 16px rgba(37,211,102,0.35); }

/* SECTION */
.section-title { font-size: 1.2rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.25rem; }
.section-sub   { font-size: 0.8rem; color: #64748b; margin-bottom: 1.25rem; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, #1a2535, transparent); margin: 1.75rem 0; }
.empty-state { text-align: center; padding: 3.5rem 2rem; color: #374151; }
.empty-state .icon { font-size: 2.5rem; margin-bottom: 0.75rem; }

/* STREAMLIT OVERRIDES */
.stButton > button {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important; font-size: 0.84rem !important;
    padding: 0.58rem 1.4rem !important;
    transition: all 0.2s !important; letter-spacing: 0.04em !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 18px rgba(16,185,129,0.32) !important; }

.stTextInput > div > div > input,
.stTextArea  > div > div > textarea {
    background: rgba(255,255,255,0.035) !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Sora', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 2px rgba(16,185,129,0.12) !important;
}
label {
    color: #7a8899 !important; font-size: 0.76rem !important;
    font-weight: 600 !important; letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    font-family: 'Sora', sans-serif !important;
}
.stSpinner > div { border-top-color: #10b981 !important; }
.stSuccess { background: rgba(16,185,129,0.08) !important; border: 1px solid rgba(16,185,129,0.25) !important; border-radius: 12px !important; color: #10b981 !important; }
.stError   { background: rgba(239,68,68,0.08) !important; border: 1px solid rgba(239,68,68,0.18) !important; border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════════════════
DB_PATH = "roziai.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS workers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, skill TEXT, city TEXT,
        experience_years INTEGER DEFAULT 0,
        daily_rate_pkr INTEGER DEFAULT 0,
        available INTEGER DEFAULT 1,
        summary TEXT, phone TEXT, transcript TEXT,
        created_at TEXT
    )''')
    conn.commit()
    count = c.execute("SELECT COUNT(*) FROM workers").fetchone()[0]
    if count == 0:
        _seed(conn)
    conn.close()

def _seed(conn):
    workers = [
        ("Ustad Zafar Ahmed",  "Plumber",      "Karachi",    15, 3000, 1, "Experienced plumber with 15 years in Karachi. Expert in pipe fitting and bathroom installations.", "923001234567"),
        ("Ali Hassan",          "Electrician",  "Lahore",      8, 2500, 1, "Skilled electrician from Lahore with 8 years experience. Handles wiring and appliance repair.", "923119876543"),
        ("Ustad Raheem Butt",   "Carpenter",    "Islamabad",  20, 4000, 0, "Master carpenter in Islamabad with 20 years of fine woodwork experience.", "923335556677"),
        ("Sajid Mehmood",       "Driver",       "Karachi",    10, 2000, 1, "Professional driver in Karachi. 10 years experience with a clean driving record.", "923212223344"),
        ("Imran Akhtar",        "Painter",      "Lahore",      6, 1800, 1, "House painter from Lahore with 6 years experience. Handles interior and exterior work.", "923441112233"),
        ("Ustad Bashir Khan",   "Plumber",      "Lahore",     12, 2800, 1, "Reliable plumber serving Lahore for 12 years. Expert in leak repairs and new installations.", "923007778899"),
        ("Tariq Hussain",       "Electrician",  "Karachi",     5, 2200, 1, "Young electrician in Karachi with 5 years experience. Available for home and commercial work.", "923138889900"),
        ("Ghulam Rasool",       "Mason",        "Rawalpindi", 18, 3500, 1, "Experienced mason in Rawalpindi with 18 years of brickwork and construction expertise.", "923315554433"),
        ("Naseer Ahmad",        "Welder",       "Faisalabad",  9, 3200, 0, "Professional welder from Faisalabad. Specialises in iron gates and industrial welding.", "923416667788"),
        ("Arif Mehmood",        "Driver",       "Islamabad",   7, 2200, 1, "Experienced driver in Islamabad. Knows all routes in the twin cities.", "923009998877"),
    ]
    c = conn.cursor()
    for w in workers:
        c.execute('''INSERT INTO workers (name,skill,city,experience_years,daily_rate_pkr,
            available,summary,phone,transcript,created_at) VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (*w, "", datetime.now().isoformat()))
    conn.commit()

def save_profile(profile: dict, transcript: str = ""):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''INSERT INTO workers (name,skill,city,experience_years,daily_rate_pkr,
        available,summary,phone,transcript,created_at) VALUES (?,?,?,?,?,?,?,?,?,?)''', (
        profile.get("name",""), profile.get("skill",""), profile.get("city",""),
        int(profile.get("experience_years",0)), int(profile.get("daily_rate_pkr",0)),
        1 if profile.get("available", True) else 0,
        profile.get("summary",""), profile.get("phone",""),
        transcript, datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def search_workers(skill_q="", city_q=""):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    q = "SELECT * FROM workers WHERE 1=1"
    params = []
    if skill_q.strip():
        q += " AND LOWER(skill) LIKE ?"
        params.append(f"%{skill_q.lower().strip()}%")
    if city_q.strip():
        q += " AND LOWER(city) LIKE ?"
        params.append(f"%{city_q.lower().strip()}%")
    q += " ORDER BY available DESC, experience_years DESC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def load_all():
    return search_workers()

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    total     = c.execute("SELECT COUNT(*) FROM workers").fetchone()[0]
    available = c.execute("SELECT COUNT(*) FROM workers WHERE available=1").fetchone()[0]
    cities    = c.execute("SELECT COUNT(DISTINCT city) FROM workers").fetchone()[0]
    skills    = c.execute("SELECT COUNT(DISTINCT skill) FROM workers").fetchone()[0]
    conn.close()
    return {"total": total, "available": available, "cities": cities, "skills": skills}


# ══════════════════════════════════════════════════════════════════════════
# AI FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════
def transcribe(audio_file) -> str:
    audio_bytes = audio_file.read()
    filename    = getattr(audio_file, "name", "audio.wav")
    resp = groq_client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=(filename, audio_bytes, "audio/wav"),
        language="ur"
    )
    return resp.text

def extract_profile(transcript: str) -> dict:
    prompt = f"""A worker in Pakistan spoke in Urdu about themselves.
Here is what they said: {transcript}

Extract the following and return ONLY valid JSON, nothing else:
{{
  "name": "their name or Not mentioned",
  "skill": "their trade e.g. plumber, electrician, carpenter, driver, painter",
  "city": "their city or Not mentioned",
  "experience_years": 0,
  "daily_rate_pkr": 0,
  "available": true,
  "summary": "2 sentence English summary",
  "phone": ""
}}"""

    resp = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.1
    )
    raw = resp.choices[0].message.content.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw).strip()
    try:
        profile = json.loads(raw)
    except Exception:
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        profile = json.loads(m.group()) if m else {}

    defaults = {"name":"Not mentioned","skill":"General labour","city":"Not mentioned",
                "experience_years":0,"daily_rate_pkr":0,"available":True,
                "summary":"Worker profile created via RoziAI.","phone":""}
    for k, v in defaults.items():
        if k not in profile:
            profile[k] = v
    return profile


# ══════════════════════════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════════════════════════
EMOJI = {"plumber":"🔧","electrician":"⚡","carpenter":"🪚","driver":"🚗",
         "painter":"🎨","mason":"🧱","welder":"🔩","cook":"🍳","tailor":"🧵"}

def skill_emoji(s):
    return EMOJI.get(s.lower().strip(), "👷")

def wa_url(phone, profile):
    phone = re.sub(r'[^0-9]', '', phone) or "92300000000"
    msg = (f"السلام علیکم! Maine RoziAI par apka profile dekha. "
           f"Mujhe {profile.get('skill','kaam')} ka kaam hai "
           f"{profile.get('city','')} mein. Kya aap available hain?")
    return f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"

def render_card(w, show_contact=True):
    avail = ('<span class="badge badge-green">✓ Available</span>'
             if w.get("available") else
             '<span class="badge badge-red">✗ Busy</span>')
    exp  = w.get("experience_years", 0)
    rate = w.get("daily_rate_pkr", 0)
    wa   = ""
    if show_contact and w.get("phone"):
        wa = f'<a class="wa-btn" href="{wa_url(w["phone"], w)}" target="_blank">📱 Contact on WhatsApp</a>'

    st.markdown(f"""
    <div class="worker-card">
        <div class="worker-avatar">{skill_emoji(w.get("skill",""))}</div>
        <div style="flex:1;min-width:0;">
            <div class="worker-name">{w.get("name","Unknown")}</div>
            <div class="worker-meta">
                <strong>{w.get("skill","").title()}</strong> &nbsp;·&nbsp;
                {w.get("city","")} &nbsp;·&nbsp; {exp} yr{"s" if exp!=1 else ""} exp
            </div>
            <div class="worker-badges">
                {avail}
                <span class="badge badge-blue">📍 {w.get("city","")}</span>
                <span class="badge badge-amber">⏱ {exp} yrs</span>
            </div>
            <div class="worker-summary">{w.get("summary","")}</div>
            <div style="margin-top:0.65rem;">{wa}</div>
        </div>
        <div class="worker-rate">PKR {rate:,}<small>per day</small></div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# INIT
# ══════════════════════════════════════════════════════════════════════════
init_db()
stats = get_stats()

# ── HERO ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="rozi-hero">
    <div class="hero-logo">Rozi<span>AI</span></div>
    <div class="hero-tagline">Connecting Pakistan's Workforce — Powered by AI</div>
    <div class="hero-urdu">ہر ہاتھ کو کام، ہر کام کو ہاتھ</div>
    <div class="stat-row">
        <div class="stat-pill">👷 {stats['total']} Workers</div>
        <div class="stat-pill">✅ {stats['available']} Available</div>
        <div class="stat-pill">🏙 {stats['cities']} Cities</div>
        <div class="stat-pill">🛠 {stats['skills']} Skills</div>
    </div>
</div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────
if "tab" not in st.session_state:
    st.session_state.tab = "worker"

col1, col2, _ = st.columns([1.2, 1.2, 5])
with col1:
    if st.button("👷 Worker Register"):
        st.session_state.tab = "worker"
with col2:
    if st.button("🔍 Find Workers"):
        st.session_state.tab = "employer"

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# TAB — WORKER REGISTER
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.tab == "worker":

    st.markdown('<div class="section-title">🎙 Worker Registration</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Speak in Urdu — our AI does the rest. No typing, no forms, no English needed.</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**Step 1 — Upload your voice recording**")
    st.markdown("""<div class="banner-info">
    📱 Record a voice note on your phone in Urdu. Say your name, skill, city, years of experience, and daily rate. Then upload it here.
    </div>""", unsafe_allow_html=True)

    st.markdown("**Example (speak something like this):**")
    st.markdown("""<div class="transcript-box">
    میرا نام زفر ہے۔ میں پلمبر ہوں۔ کراچی میں رہتا ہوں۔ پندرہ سال کا تجربہ ہے۔ روز کا کرایہ تین ہزار روپے ہے۔
    </div>""", unsafe_allow_html=True)

    audio_file = st.file_uploader(
        "Upload audio (MP3, WAV, M4A, OGG)",
        type=["wav","mp3","m4a","ogg","webm"]
    )

    st.markdown("**— OR type / paste Urdu text directly —**")
    manual = st.text_area(
        "Urdu text",
        placeholder="مثال: میرا نام علی ہے۔ میں الیکٹریشن ہوں۔ لاہور میں رہتا ہوں۔",
        height=100
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**Step 2 — Phone number (for WhatsApp contact)**")
    phone = st.text_input("Phone number with country code", placeholder="e.g. 923001234567")
    st.markdown('</div>', unsafe_allow_html=True)

    if "transcript" not in st.session_state:
        st.session_state.transcript = ""
    if "profile" not in st.session_state:
        st.session_state.profile = None

    if st.button("✨ Build My Profile with AI"):
        text = ""
        if audio_file:
            with st.spinner("🎙 Transcribing audio with Groq Whisper..."):
                try:
                    text = transcribe(audio_file)
                    st.session_state.transcript = text
                except Exception as e:
                    st.error(f"Transcription failed: {e}")
                    st.stop()
        elif manual.strip():
            text = manual.strip()
            st.session_state.transcript = text
        else:
            st.warning("Please upload an audio file or type some text.")
            st.stop()

        with st.spinner("🤖 Extracting profile with Llama AI..."):
            try:
                p = extract_profile(text)
                if phone.strip():
                    p["phone"] = re.sub(r'[^0-9]', '', phone)
                st.session_state.profile = p
            except Exception as e:
                st.error(f"Profile extraction failed: {e}")
                st.stop()

    if st.session_state.transcript:
        st.markdown("**Urdu Transcript:**")
        st.markdown(f'<div class="transcript-box">{st.session_state.transcript}</div>',
                    unsafe_allow_html=True)

    if st.session_state.profile:
        p = st.session_state.profile
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="banner-success">✅ Profile built! Review below then save.</div>',
                    unsafe_allow_html=True)
        st.markdown("**Preview:**")
        render_card(p, show_contact=False)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**Edit if needed:**")
        c1, c2 = st.columns(2)
        with c1:
            p["name"]  = st.text_input("Name",  value=p.get("name",""))
            p["skill"] = st.text_input("Skill", value=p.get("skill",""))
            p["city"]  = st.text_input("City",  value=p.get("city",""))
        with c2:
            p["experience_years"] = st.number_input("Years Experience", value=int(p.get("experience_years",0)), min_value=0, max_value=60)
            p["daily_rate_pkr"]   = st.number_input("Daily Rate PKR",   value=int(p.get("daily_rate_pkr",0)),   min_value=0, step=100)
            p["available"]        = st.checkbox("Currently Available", value=bool(p.get("available",True)))
        p["summary"] = st.text_area("Summary", value=p.get("summary",""))
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("💾 Save Profile"):
            save_profile(p, st.session_state.transcript)
            st.success(f"🎉 Profile for {p['name']} saved!")
            st.session_state.profile = None
            st.session_state.transcript = ""
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════
# TAB — FIND WORKERS
# ══════════════════════════════════════════════════════════════════════════
else:
    st.markdown('<div class="section-title">🔍 Find Skilled Workers</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Search by skill and city. Contact instantly via WhatsApp.</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        skill_q = st.text_input("Skill needed", placeholder="e.g. plumber, electrician")
    with c2:
        city_q  = st.text_input("City", placeholder="e.g. Karachi, Lahore")
    with c3:
        st.markdown('<div style="height:28px"></div>', unsafe_allow_html=True)
        search  = st.button("Search 🔍")

    # Quick chips
    st.markdown('<div style="margin-top:0.5rem; font-size:0.72rem; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; font-weight:600;">Quick search:</div>', unsafe_allow_html=True)
    chips = ["Plumber","Electrician","Carpenter","Driver","Painter","Mason","Welder","Cook"]
    cols  = st.columns(len(chips))
    for i, ch in enumerate(chips):
        with cols[i]:
            if st.button(f"{skill_emoji(ch)} {ch}", key=f"chip_{ch}"):
                skill_q = ch
                search  = True

    st.markdown('</div>', unsafe_allow_html=True)

    results = search_workers(skill_q, city_q) if (search or skill_q or city_q) else load_all()

    label = f'Results for "{skill_q}"' if skill_q else "All Workers"
    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;">
        <span style="font-size:1rem;font-weight:700;color:#f1f5f9;">{label}</span>
        <span style="font-size:0.78rem;color:#64748b;">{len(results)} found</span>
    </div>""", unsafe_allow_html=True)

    if not results:
        st.markdown('<div class="empty-state"><div class="icon">🔍</div><p>No workers found. Try a different skill or city.</p></div>',
                    unsafe_allow_html=True)
    else:
        for w in results:
            render_card(w, show_contact=True)
     