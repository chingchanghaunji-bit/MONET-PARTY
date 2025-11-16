
import sqlite3
from datetime import datetime

DB_PATH = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS allowed (
                    email TEXT PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    registered INTEGER DEFAULT 0,
                    ticket_id TEXT,
                    verified INTEGER DEFAULT 0,
                    created_at TEXT,
                    registered_at TEXT,
                    verified_at TEXT
                )""")
    
    # Add missing columns if they don't exist (for existing databases)
    try:
        c.execute("ALTER TABLE allowed ADD COLUMN created_at TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        c.execute("ALTER TABLE allowed ADD COLUMN registered_at TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        c.execute("ALTER TABLE allowed ADD COLUMN verified_at TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    conn.close()

def get_user(email=None, ticket_id=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if email:
        c.execute("SELECT * FROM allowed WHERE email=?", (email,))
    else:
        c.execute("SELECT * FROM allowed WHERE ticket_id=?", (ticket_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "email": row[0],
            "name": row[1],
            "phone": row[2],
            "registered": row[3],
            "ticket_id": row[4],
            "verified": row[5],
            "created_at": row[6] if len(row) > 6 else None,
            "registered_at": row[7] if len(row) > 7 else None,
            "verified_at": row[8] if len(row) > 8 else None
        }
    return None

def add_user(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT OR IGNORE INTO allowed (email, created_at) VALUES (?, ?)", (email, now))
    conn.commit()
    conn.close()

def update_user(email, **kwargs):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for key, value in kwargs.items():
        c.execute(f"UPDATE allowed SET {key}=? WHERE email=?", (value, email))
    conn.commit()
    conn.close()

def fetch_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Check if created_at column exists, if not order by email
    try:
        c.execute("SELECT * FROM allowed ORDER BY created_at DESC")
    except sqlite3.OperationalError:
        # Fallback if created_at doesn't exist
        c.execute("SELECT * FROM allowed ORDER BY email")
    rows = c.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    total = c.execute("SELECT COUNT(*) FROM allowed").fetchone()[0]
    registered = c.execute("SELECT COUNT(*) FROM allowed WHERE registered=1").fetchone()[0]
    verified = c.execute("SELECT COUNT(*) FROM allowed WHERE verified=1").fetchone()[0]
    pending = total - registered
    
    conn.close()
    return {
        "total": total,
        "registered": registered,
        "verified": verified,
        "pending": pending
    }
