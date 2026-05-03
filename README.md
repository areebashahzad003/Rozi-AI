# RoziAI 🔧
### *Har Haath Ko Kaam — ہر ہاتھ کو کام*
**Connecting Pakistan's 40 million invisible workers to the modern economy — via voice, in Urdu.**

---

## What It Does

1. **Worker speaks in Urdu** → uploads a voice recording
2. **Groq Whisper** transcribes speech to Urdu text (2 seconds)
3. **Claude AI** reads the transcript and extracts a structured profile (name, skill, city, experience, rate)
4. **Profile card** is generated and saved to the database
5. **Employers search** by skill + city and contact workers via **WhatsApp in one tap**

---

## Quick Start

### 1. Clone and enter the project
```bash
git clone <your-repo-url>
cd roziai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```
> If `pyaudio` fails on Windows: `pip install pipwin && pipwin install pyaudio`  
> On Ubuntu/Debian: `sudo apt-get install portaudio19-dev` first

### 3. Add your API keys
```bash
cp .env.example .env
# Edit .env and paste your actual keys
```

**Get keys (both free):**
- Groq: https://console.groq.com → API Keys
- Anthropic: https://console.anthropic.com → API Keys

### 4. Run the app
```bash
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## Project Structure

```
roziai/
├── app.py          ← Main Streamlit app (UI, routing, layout)
├── voice.py        ← Audio recording + Groq Whisper transcription
├── profile.py      ← Claude API — extract structured profile from Urdu text
├── storage.py      ← SQLite database (save, load, search workers)
├── requirements.txt
├── .env.example    ← Copy to .env and add your keys
└── README.md
```

---

## Team Responsibilities

| Member | Role | Files |
|--------|------|-------|
| Member 1 | Voice & AI Lead | `voice.py`, `profile.py` |
| Member 2 | Frontend Lead | UI sections in `app.py` |
| Member 3 | Data & Testing | `storage.py`, test profiles |
| Member 4 | Integration Lead | `app.py` (main), `README.md` |

---

## Demo Script (memorise this)

> *"Meet Ustad Zafar. He is a plumber from Karachi. He cannot read or write English. He cannot make a CV. Watch what happens."*

1. Go to **Worker Register** tab
2. Upload audio of: *"Mera naam Zafar hai. Main plumber hoon. Karachi mein rehta hoon. Pandra saal ka tajruba hai. Roz ka kiraya teen hazaar rupay hai."*
3. Click **Build My Profile with AI**
4. Show the profile card that appears
5. Click **Save Profile**
6. Switch to **Find Workers** tab
7. Search: skill = `plumber`, city = `Karachi`
8. His card appears → tap **Contact on WhatsApp**

> *"We gave 40 million invisible workers a voice."*

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI |
| Groq Whisper | Urdu speech-to-text |
| Claude (Anthropic) | Profile extraction from transcript |
| SQLite | Local database |

---

## Common Issues

**`ModuleNotFoundError`** → `pip install -r requirements.txt`

**`Invalid API Key`** → Check your `.env` file, make sure `load_dotenv()` is called

**`JSON decode error from Claude`** → Rare; retry. Claude occasionally adds preamble — the code strips markdown fences automatically.

**`pyaudio` install fails** → Use the file upload feature instead of live recording (works in all browsers)

---

## Scaling Beyond Hackathon
- Replace SQLite with PostgreSQL for production
- Deploy to Railway, Render, or Heroku (one command)
- Add user auth with Streamlit-Authenticator
- Add SMS notifications via Twilio

---

*Built for hackathon. Built for Pakistan. Built with ❤️*
