import streamlit as st
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title='RoziAI — Har Haath Ko Kaam',
    page_icon='🔧',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# ── Lazy imports after env is loaded ──────────────────────────────────────
from storage import init_db, save_profile, load_all_profiles, search_workers, get_stats
from profile import extract_profile
from voice import transcribe_audio_file

init_db()

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&family=Sora:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0a0c10 !important;
    color: #e8eaf0 !important;
    font-family: 'Sora', sans-serif !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }

/* ── HERO HEADER ── */
.rozi-hero {
    background: linear-gradient(135deg, #0d1117 0%, #111827 50%, #0d1117 100%);
    border-bottom: 1px solid #1e2a3a;
    padding: 2.5rem 3rem 2rem;
    position: relative;
    overflow: hidden;
}
.rozi-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(16,185,129,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.rozi-hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 200px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-logo {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #f0f4f8;
    line-height: 1;
}
.hero-logo span { color: #10b981; }
.hero-tagline {
    font-size: 0.85rem;
    color: #6b7a8d;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.hero-urdu {
    font-family: 'Noto Nastaliq Urdu', serif;
    font-size: 1.1rem;
    color: #10b981;
    direction: rtl;
    margin-top: 0.2rem;
}

/* ── STAT PILLS ── */
.stat-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.5rem;
    flex-wrap: wrap;
}
.stat-pill {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-size: 0.78rem;
    color: #10b981;
    font-weight: 600;
    letter-spacing: 0.04em;
}

/* ── TAB NAV ── */
.tab-nav {
    display: flex;
    gap: 0;
    padding: 1.5rem 3rem 0;
    border-bottom: 1px solid #1e2a3a;
    background: #0d1117;
}
.tab-btn {
    padding: 0.65rem 1.8rem;
    font-family: 'Sora', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    background: transparent;
    color: #6b7a8d;
    letter-spacing: 0.04em;
    transition: all 0.2s;
}
.tab-btn.active {
    color: #10b981;
    border-bottom-color: #10b981;
}

/* ── MAIN LAYOUT ── */
.main-content {
    padding: 2rem 3rem;
    max-width: 1200px;
}

/* ── SECTION TITLES ── */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f0f4f8;
    margin-bottom: 0.3rem;
}
.section-sub {
    font-size: 0.82rem;
    color: #6b7a8d;
    margin-bottom: 1.5rem;
}

/* ── CARDS ── */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid #1e2a3a;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.glass-card:hover { border-color: rgba(16,185,129,0.3); }

/* ── WORKER PROFILE CARD ── */
.worker-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid #1e2a3a;
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
    box-shadow: 0 8px 32px rgba(16,185,129,0.08);
}
.worker-avatar {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #10b981, #6366f1);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
}
.worker-name {
    font-size: 1rem;
    font-weight: 700;
    color: #f0f4f8;
    margin-bottom: 0.2rem;
}
.worker-meta {
    font-size: 0.78rem;
    color: #8892a4;
    margin-bottom: 0.5rem;
}
.worker-meta strong { color: #b0bac9; }
.worker-badges {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 0.4rem;
}
.badge {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.2rem 0.65rem;
    border-radius: 100px;
    letter-spacing: 0.03em;
}
.badge-green {
    background: rgba(16,185,129,0.12);
    color: #10b981;
    border: 1px solid rgba(16,185,129,0.25);
}
.badge-blue {
    background: rgba(99,102,241,0.12);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.25);
}
.badge-orange {
    background: rgba(245,158,11,0.12);
    color: #fbbf24;
    border: 1px solid rgba(245,158,11,0.25);
}
.badge-red {
    background: rgba(239,68,68,0.1);
    color: #f87171;
    border: 1px solid rgba(239,68,68,0.2);
}
.worker-summary {
    font-size: 0.8rem;
    color: #6b7a8d;
    margin-top: 0.4rem;
    line-height: 1.5;
}
.worker-rate {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.05rem;
    font-weight: 600;
    color: #10b981;
    margin-left: auto;
    text-align: right;
    white-space: nowrap;
    padding-left: 1rem;
}
.worker-rate small {
    display: block;
    font-size: 0.65rem;
    color: #6b7a8d;
    font-weight: 400;
    margin-top: 0.1rem;
}

/* ── TRANSCRIPT BOX ── */
.transcript-box {
    background: rgba(255,255,255,0.02);
    border: 1px solid #2a3a4a;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-family: 'Noto Nastaliq Urdu', serif;
    font-size: 1.1rem;
    direction: rtl;
    color: #c8d0dc;
    line-height: 1.8;
    min-height: 80px;
}

/* ── SUCCESS / INFO BANNERS ── */
.banner-success {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-size: 0.85rem;
    color: #10b981;
    margin: 1rem 0;
}
.banner-info {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-size: 0.85rem;
    color: #818cf8;
    margin: 1rem 0;
}
.banner-warn {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 12px;
    padding: 0.85rem 1.2rem;
    font-size: 0.85rem;
    color: #fbbf24;
    margin: 1rem 0;
}

/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
    background: linear-gradient(135deg, #10b981, #059669) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.04em !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(16,185,129,0.35) !important;
}
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid #2a3a4a !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
    font-family: 'Sora', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 2px rgba(16,185,129,0.15) !important;
}
.stFileUploader {
    background: rgba(255,255,255,0.02) !important;
    border: 2px dashed #2a3a4a !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid #2a3a4a !important;
    border-radius: 10px !important;
    color: #e8eaf0 !important;
}
label, .stTextInput label, .stTextArea label, .stFileUploader label {
    color: #8892a4 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-family: 'Sora', sans-serif !important;
}
.stAudio { margin-top: 0.5rem; }
.stSpinner > div { border-top-color: #10b981 !important; }
.stSuccess {
    background: rgba(16,185,129,0.1) !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 12px !important;
    color: #10b981 !important;
}
.stError {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.2) !important;
    border-radius: 12px !important;
}
div[data-testid="stHorizontalBlock"] { gap: 1rem; }
.stMarkdown p { color: #8892a4; }
hr { border-color: #1e2a3a !important; }

/* ── SEARCH BAR ── */
.search-wrap {
    background: rgba(255,255,255,0.03);
    border: 1px solid #1e2a3a;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #4a5568;
}
.empty-state .icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state p { font-size: 0.9rem; }

/* ── WHATSAPP BUTTON ── */
.wa-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #25D366;
    color: #fff !important;
    text-decoration: none !important;
    font-family: 'Sora', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.4rem 0.9rem;
    border-radius: 100px;
    letter-spacing: 0.04em;
    transition: all 0.2s;
}
.wa-btn:hover {
    background: #1da851;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(37,211,102,0.4);
}

/* ── DIVIDER ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e2a3a, transparent);
    margin: 2rem 0;
}

/* ── SKILL FILTER CHIPS ── */
.chip-row { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
.chip {
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 600;
    background: rgba(255,255,255,0.05);
    border: 1px solid #2a3a4a;
    color: #8892a4;
    cursor: pointer;
    transition: all 0.2s;
}
.chip:hover { border-color: #10b981; color: #10b981; }
</style>
""", unsafe_allow_html=True)


# ── SKILL EMOJI MAP ──────────────────────────────────────────────────────
SKILL_EMOJI = {
    'plumber': '🔧', 'electrician': '⚡', 'carpenter': '🪚',
    'driver': '🚗', 'painter': '🎨', 'mason': '🧱',
    'welder': '🔩', 'mechanic': '🔩', 'tailor': '🧵',
    'cook': '🍳', 'gardener': '🌿', 'cleaner': '🧹',
    'ac technician': '❄️', 'mobile repair': '📱',
}


def skill_emoji(skill: str) -> str:
    return SKILL_EMOJI.get(skill.lower().strip(), '👷')


def whatsapp_url(phone: str, profile: dict) -> str:
    phone = phone.strip().replace('+', '').replace('-', '').replace(' ', '')
    if not phone:
        phone = '92300000000'
    msg = (
        f"السلام علیکم! Maine RoziAI par apka profile dekha. "
        f"Mujhe {profile.get('skill','kaam')} ka kaam hai "
        f"{profile.get('city','')} mein. Kya aap available hain?"
    )
    return f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"


def render_worker_card(w: dict, show_contact: bool = True):
    avail_badge = (
        '<span class="badge badge-green">✓ Available</span>'
        if w.get('available') else
        '<span class="badge badge-red">✗ Busy</span>'
    )
    exp = w.get('experience_years', 0)
    rate = w.get('daily_rate_pkr', 0)

    wa_html = ''
    if show_contact and w.get('phone'):
        wa_html = f'''<a class="wa-btn" href="{whatsapp_url(w['phone'], w)}" target="_blank">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
            </svg>
            Contact on WhatsApp
        </a>'''

    st.markdown(f"""
    <div class="worker-card">
        <div class="worker-avatar">{skill_emoji(w.get('skill',''))}</div>
        <div style="flex:1; min-width:0;">
            <div class="worker-name">{w.get('name','Unknown Worker')}</div>
            <div class="worker-meta">
                <strong>{w.get('skill','').title()}</strong> &nbsp;·&nbsp;
                {w.get('city','')} &nbsp;·&nbsp;
                {exp} yr{'s' if exp != 1 else ''} exp
            </div>
            <div class="worker-badges">
                {avail_badge}
                <span class="badge badge-blue">📍 {w.get('city','')}</span>
                <span class="badge badge-orange">⏱ {exp} yrs</span>
            </div>
            <div class="worker-summary">{w.get('summary','')}</div>
            <div style="margin-top:0.7rem;">{wa_html}</div>
        </div>
        <div class="worker-rate">
            PKR {rate:,}
            <small>per day</small>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── HEADER ────────────────────────────────────────────────────────────────
stats = get_stats()
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
</div>
""", unsafe_allow_html=True)

# ── TAB SWITCHER ──────────────────────────────────────────────────────────
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'worker'

col_t1, col_t2, col_t3 = st.columns([1, 1, 4])
with col_t1:
    if st.button('👷 Worker Register', key='tab_worker'):
        st.session_state.active_tab = 'worker'
with col_t2:
    if st.button('🔍 Find Workers', key='tab_employer'):
        st.session_state.active_tab = 'employer'

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB: WORKER REGISTRATION
# ═══════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == 'worker':

    st.markdown("""
    <div style="padding: 0 0 0.5rem;">
        <div class="section-title">🎙 Worker Registration</div>
        <div class="section-sub">Speak in Urdu — our AI does the rest. No typing, no forms, no English needed.</div>
    </div>
    """, unsafe_allow_html=True)

    # ── STEP 1: Voice Input ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**Step 1 — Upload Your Voice Recording**")
    st.markdown("""
    <div class="banner-info">
    📱 <strong>How to record:</strong> Use your phone's voice memo app, WhatsApp voice note, or any recorder.
    Speak in Urdu about yourself — say your name, skill, city, years of experience, and daily rate.
    Then upload the file here.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Example (say something like this):**")
    st.markdown("""
    <div class="transcript-box">
    میرا نام زفر ہے۔ میں پلمبر ہوں۔ کراچی میں رہتا ہوں۔ پندرہ سال کا تجربہ ہے۔ روز کا کرایہ تین ہزار روپے ہے۔
    </div>
    """, unsafe_allow_html=True)

    audio_file = st.file_uploader(
        'Upload audio file (MP3, WAV, M4A, OGG)',
        type=['wav', 'mp3', 'm4a', 'ogg', 'webm'],
        key='audio_upload'
    )

    st.markdown("**— OR enter Urdu text directly —**")
    manual_text = st.text_area(
        'Type / paste Urdu text here',
        placeholder='مثال: میرا نام علی ہے۔ میں الیکٹریشن ہوں۔ لاہور میں رہتا ہوں۔ آٹھ سال کا تجربہ ہے۔',
        height=100,
        key='manual_text'
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── STEP 2: Optional phone ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**Step 2 — Phone Number (for WhatsApp contact)**")
    phone_input = st.text_input(
        'Phone number (with country code)',
        placeholder='e.g. 923001234567',
        key='phone_input'
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── BUILD PROFILE BUTTON ──
    build_btn = st.button('✨ Build My Profile with AI', key='build_btn')

    if 'transcript' not in st.session_state:
        st.session_state.transcript = ''
    if 'built_profile' not in st.session_state:
        st.session_state.built_profile = None

    if build_btn:
        transcript = ''

        # Get transcript from audio or manual text
        if audio_file is not None:
            with st.spinner('🎙 Transcribing audio with Groq Whisper...'):
                try:
                    transcript = transcribe_audio_file(audio_file)
                    st.session_state.transcript = transcript
                except Exception as e:
                    st.error(f'Transcription failed: {e}')
                    st.stop()
        elif manual_text.strip():
            transcript = manual_text.strip()
            st.session_state.transcript = transcript
        else:
            st.warning('Please upload an audio file or enter text.')
            st.stop()

        # Extract profile with Claude
        with st.spinner('🤖 Extracting profile with Claude AI...'):
            try:
                profile = extract_profile(transcript)
                if phone_input.strip():
                    profile['phone'] = phone_input.strip().replace('+', '').replace(' ', '').replace('-', '')
                st.session_state.built_profile = profile
            except Exception as e:
                st.error(f'Profile extraction failed: {e}')
                st.stop()

    # ── SHOW TRANSCRIPT ──
    if st.session_state.transcript:
        st.markdown("**Urdu Transcript:**")
        st.markdown(f'<div class="transcript-box">{st.session_state.transcript}</div>', unsafe_allow_html=True)

    # ── SHOW BUILT PROFILE ──
    if st.session_state.built_profile:
        profile = st.session_state.built_profile
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="banner-success">
        ✅ Profile built successfully! Review below, then save it.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Your Profile Card (preview):**")
        render_worker_card(profile, show_contact=False)

        # Editable fields
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("**Review & Edit (optional):**")
        c1, c2 = st.columns(2)
        with c1:
            profile['name'] = st.text_input('Name', value=profile.get('name', ''), key='edit_name')
            profile['skill'] = st.text_input('Skill', value=profile.get('skill', ''), key='edit_skill')
            profile['city'] = st.text_input('City', value=profile.get('city', ''), key='edit_city')
        with c2:
            profile['experience_years'] = st.number_input(
                'Years of Experience', value=int(profile.get('experience_years', 0)),
                min_value=0, max_value=60, key='edit_exp'
            )
            profile['daily_rate_pkr'] = st.number_input(
                'Daily Rate (PKR)', value=int(profile.get('daily_rate_pkr', 0)),
                min_value=0, step=100, key='edit_rate'
            )
            profile['available'] = st.checkbox(
                'Currently Available', value=bool(profile.get('available', True)), key='edit_avail'
            )

        profile['summary'] = st.text_area(
            'Profile Summary (English)', value=profile.get('summary', ''), key='edit_summary'
        )
        st.markdown('</div>', unsafe_allow_html=True)

        save_btn = st.button('💾 Save Profile to RoziAI', key='save_btn')
        if save_btn:
            try:
                save_profile(profile, transcript=st.session_state.transcript)
                st.success(f"🎉 Profile for **{profile['name']}** saved successfully!")
                st.markdown("""
                <div class="banner-success">
                Employers can now find this worker by searching their skill and city.
                </div>
                """, unsafe_allow_html=True)
                st.session_state.built_profile = None
                st.session_state.transcript = ''
                st.rerun()
            except Exception as e:
                st.error(f'Save failed: {e}')


# ═══════════════════════════════════════════════════════════════════════════
# TAB: EMPLOYER SEARCH
# ═══════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == 'employer':

    st.markdown("""
    <div style="padding: 0 0 0.5rem;">
        <div class="section-title">🔍 Find Skilled Workers</div>
        <div class="section-sub">Search by skill and city. Contact instantly via WhatsApp.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="search-wrap">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        skill_q = st.text_input('Skill needed', placeholder='e.g. plumber, electrician, driver', key='skill_q')
    with c2:
        city_q = st.text_input('City', placeholder='e.g. Karachi, Lahore, Islamabad', key='city_q')
    with c3:
        st.markdown('<div style="height:28px;"></div>', unsafe_allow_html=True)
        search_clicked = st.button('Search 🔍', key='search_btn')

    # Quick skill chips
    st.markdown("""
    <div style="margin-top:0.5rem;">
        <span style="font-size:0.75rem; color:#6b7a8d; text-transform:uppercase; letter-spacing:0.08em; font-weight:600;">Quick search:</span>
    </div>
    """, unsafe_allow_html=True)

    chip_cols = st.columns(8)
    quick_skills = ['Plumber', 'Electrician', 'Carpenter', 'Driver', 'Painter', 'Mason', 'Welder', 'Cook']
    for i, qs in enumerate(quick_skills):
        with chip_cols[i]:
            if st.button(f'{skill_emoji(qs)} {qs}', key=f'chip_{qs}'):
                st.session_state['skill_q_val'] = qs
                skill_q = qs
                search_clicked = True

    st.markdown('</div>', unsafe_allow_html=True)

    # Run search
    if search_clicked or skill_q or city_q:
        results = search_workers(skill_q, city_q)
    else:
        results = load_all_profiles()

    # Results header
    result_label = 'All Workers' if not skill_q and not city_q else f'Results for "{skill_q}" in "{city_q}"'
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
        <div>
            <span style="font-size:1rem; font-weight:700; color:#f0f4f8;">{result_label}</span>
            <span style="font-size:0.8rem; color:#6b7a8d; margin-left:0.75rem;">{len(results)} found</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not results:
        st.markdown("""
        <div class="empty-state">
            <div class="icon">🔍</div>
            <p>No workers found matching your search.<br>Try a different skill or city.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for w in results:
            render_worker_card(w, show_contact=True)
