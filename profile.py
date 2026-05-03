import os
import json
import re
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def extract_profile(urdu_transcript: str) -> dict:
    prompt = f"""A worker in Pakistan spoke in Urdu about themselves.
Here is what they said: {urdu_transcript}

Extract the following fields and return ONLY valid JSON (no markdown, no explanation):
{{
  "name": "their name, or Not mentioned if missing",
  "skill": "their trade e.g. plumber, electrician, carpenter, driver, painter",
  "city": "their city, or Not mentioned if missing",
  "experience_years": 0,
  "daily_rate_pkr": 0,
  "available": true,
  "summary": "2 sentence English summary of their profile",
  "phone": ""
}}

Return ONLY the JSON object, nothing else."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
        temperature=0.1
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r'^```(?:json)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    raw = raw.strip()

    try:
        profile = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            profile = json.loads(match.group())
        else:
            raise ValueError(f"Could not parse response: {raw}")

    defaults = {
        'name': 'Not mentioned',
        'skill': 'General labour',
        'city': 'Not mentioned',
        'experience_years': 0,
        'daily_rate_pkr': 0,
        'available': True,
        'summary': 'Worker profile created via RoziAI.',
        'phone': ''
    }
    for key, default in defaults.items():
        if key not in profile:
            profile[key] = default

    return profile