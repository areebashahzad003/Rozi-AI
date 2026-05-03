import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'roziai.db')


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist and seed demo data."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skill TEXT NOT NULL,
            city TEXT NOT NULL,
            experience_years INTEGER DEFAULT 0,
            daily_rate_pkr INTEGER DEFAULT 0,
            available INTEGER DEFAULT 1,
            summary TEXT,
            phone TEXT,
            transcript TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()

    # Seed demo data if empty
    count = cursor.execute('SELECT COUNT(*) FROM workers').fetchone()[0]
    if count == 0:
        _seed_demo_data(conn)

    conn.close()


def _seed_demo_data(conn):
    demo_workers = [
        {
            'name': 'Ustad Zafar Ahmed',
            'skill': 'Plumber',
            'city': 'Karachi',
            'experience_years': 15,
            'daily_rate_pkr': 3000,
            'available': 1,
            'summary': 'Experienced plumber with 15 years in Karachi. Specialises in pipe fitting and bathroom installations.',
            'phone': '923001234567',
            'transcript': 'Mera naam Zafar hai. Main plumber hoon. Karachi mein rehta hoon. Pandra saal ka tajruba hai.'
        },
        {
            'name': 'Ali Hassan',
            'skill': 'Electrician',
            'city': 'Lahore',
            'experience_years': 8,
            'daily_rate_pkr': 2500,
            'available': 1,
            'summary': 'Skilled electrician from Lahore with 8 years experience. Handles wiring, panels and appliance repair.',
            'phone': '923119876543',
            'transcript': 'Main Ali hoon. Electrician ka kaam karta hoon Lahore mein. Aath saal se kaam kar raha hoon.'
        },
        {
            'name': 'Ustad Raheem Butt',
            'skill': 'Carpenter',
            'city': 'Islamabad',
            'experience_years': 20,
            'daily_rate_pkr': 4000,
            'available': 0,
            'summary': 'Master carpenter based in Islamabad with 20 years of fine woodwork experience.',
            'phone': '923335556677',
            'transcript': 'Mera naam Raheem hai. Barhai ka kaam karta hoon. Islamabad mein hoon.'
        },
        {
            'name': 'Sajid Mehmood',
            'skill': 'Driver',
            'city': 'Karachi',
            'experience_years': 10,
            'daily_rate_pkr': 2000,
            'available': 1,
            'summary': 'Professional driver in Karachi. 10 years experience with clean driving record.',
            'phone': '923212223344',
            'transcript': 'Main driver hoon Karachi mein. Dus saal ka experience hai.'
        },
        {
            'name': 'Imran Akhtar',
            'skill': 'Painter',
            'city': 'Lahore',
            'experience_years': 6,
            'daily_rate_pkr': 1800,
            'available': 1,
            'summary': 'House painter from Lahore with 6 years experience. Handles interior and exterior work.',
            'phone': '923441112233',
            'transcript': 'Mera naam Imran hai. Rang kari karta hoon. Chhe saal ka kaam hai.'
        },
        {
            'name': 'Ustad Bashir Khan',
            'skill': 'Plumber',
            'city': 'Lahore',
            'experience_years': 12,
            'daily_rate_pkr': 2800,
            'available': 1,
            'summary': 'Reliable plumber serving Lahore for 12 years. Expert in leak repairs and new installations.',
            'phone': '923007778899',
            'transcript': 'Naam Bashir hai. Plumber hoon. Bara saal se Lahore mein kaam kar raha hoon.'
        },
        {
            'name': 'Tariq Hussain',
            'skill': 'Electrician',
            'city': 'Karachi',
            'experience_years': 5,
            'daily_rate_pkr': 2200,
            'available': 1,
            'summary': 'Young electrician in Karachi with 5 years experience. Available for home and commercial work.',
            'phone': '923138889900',
            'transcript': 'Main Tariq hoon. Electrician hoon Karachi mein.'
        },
        {
            'name': 'Ghulam Rasool',
            'skill': 'Mason',
            'city': 'Rawalpindi',
            'experience_years': 18,
            'daily_rate_pkr': 3500,
            'available': 1,
            'summary': 'Experienced mason in Rawalpindi with 18 years of brickwork and construction expertise.',
            'phone': '923315554433',
            'transcript': 'Mera naam Ghulam Rasool hai. Raj mistri hoon. Rawalpindi mein hoon.'
        },
        {
            'name': 'Naseer Ahmad',
            'skill': 'Welder',
            'city': 'Faisalabad',
            'experience_years': 9,
            'daily_rate_pkr': 3200,
            'available': 0,
            'summary': 'Professional welder from Faisalabad. Specialises in iron gates, grills and industrial welding.',
            'phone': '923416667788',
            'transcript': 'Naseer hoon. Welder hoon Faisalabad mein. Nau saal ka kaam hai.'
        },
        {
            'name': 'Arif Mehmood',
            'skill': 'Driver',
            'city': 'Islamabad',
            'experience_years': 7,
            'daily_rate_pkr': 2200,
            'available': 1,
            'summary': 'Experienced driver in Islamabad available for daily hire. Knows all routes in twin cities.',
            'phone': '923009998877',
            'transcript': 'Mera naam Arif hai. Main driver hoon Islamabad mein. Saat saal ka tajruba hai.'
        },
    ]

    cursor = conn.cursor()
    for w in demo_workers:
        cursor.execute('''
            INSERT INTO workers (name, skill, city, experience_years, daily_rate_pkr,
                available, summary, phone, transcript, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            w['name'], w['skill'], w['city'], w['experience_years'],
            w['daily_rate_pkr'], w['available'], w['summary'],
            w['phone'], w['transcript'], datetime.now().isoformat()
        ))
    conn.commit()


def save_profile(profile: dict, transcript: str = '') -> int:
    """Save a worker profile. Returns the new row ID."""
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workers (name, skill, city, experience_years, daily_rate_pkr,
            available, summary, phone, transcript, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        profile.get('name', ''),
        profile.get('skill', ''),
        profile.get('city', ''),
        int(profile.get('experience_years', 0)),
        int(profile.get('daily_rate_pkr', 0)),
        1 if profile.get('available', True) else 0,
        profile.get('summary', ''),
        profile.get('phone', ''),
        transcript,
        datetime.now().isoformat()
    ))
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id


def load_all_profiles() -> list:
    """Return all worker profiles as a list of dicts."""
    conn = _get_connection()
    cursor = conn.cursor()
    rows = cursor.execute(
        'SELECT * FROM workers ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def search_workers(skill_query: str = '', city_query: str = '') -> list:
    """Search workers by skill and/or city."""
    conn = _get_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM workers WHERE 1=1'
    params = []

    if skill_query.strip():
        query += ' AND LOWER(skill) LIKE ?'
        params.append(f'%{skill_query.lower().strip()}%')

    if city_query.strip():
        query += ' AND LOWER(city) LIKE ?'
        params.append(f'%{city_query.lower().strip()}%')

    query += ' ORDER BY available DESC, experience_years DESC'
    rows = cursor.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_stats() -> dict:
    """Return summary stats for the dashboard."""
    conn = _get_connection()
    cursor = conn.cursor()
    total = cursor.execute('SELECT COUNT(*) FROM workers').fetchone()[0]
    available = cursor.execute('SELECT COUNT(*) FROM workers WHERE available=1').fetchone()[0]
    cities = cursor.execute('SELECT COUNT(DISTINCT city) FROM workers').fetchone()[0]
    skills = cursor.execute('SELECT COUNT(DISTINCT skill) FROM workers').fetchone()[0]
    conn.close()
    return {
        'total': total,
        'available': available,
        'cities': cities,
        'skills': skills
    }
