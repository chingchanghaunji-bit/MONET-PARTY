#!/usr/bin/env python
"""
Database Check and Recovery Script
Run this to check database status and recover data
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = 'database.db'

def check_database():
    """Check database status and show all data"""
    if not os.path.exists(DB_PATH):
        print("[ERROR] Database file not found!")
        return
    
    print(f"[OK] Database file found: {DB_PATH}")
    print(f"   Size: {os.path.getsize(DB_PATH)} bytes")
    print(f"   Modified: {datetime.fromtimestamp(os.path.getmtime(DB_PATH))}")
    print()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Get total count
        total = c.execute("SELECT COUNT(*) FROM allowed").fetchone()[0]
        print(f"[INFO] Total Users: {total}")
        
        # Get registered count
        registered = c.execute("SELECT COUNT(*) FROM allowed WHERE registered=1").fetchone()[0]
        print(f"[INFO] Registered: {registered}")
        
        # Get verified count
        verified = c.execute("SELECT COUNT(*) FROM allowed WHERE verified=1").fetchone()[0]
        print(f"[INFO] Verified: {verified}")
        print()
        
        # Get all users
        c.execute("SELECT * FROM allowed ORDER BY created_at DESC")
        rows = c.fetchall()
        
        if rows:
            print(f"[INFO] All Users ({len(rows)} total):")
            print("=" * 100)
            print(f"{'Email':<30} {'Name':<20} {'Phone':<18} {'Ticket ID':<12} {'Registered':<12} {'Verified':<12}")
            print("-" * 100)
            
            for row in rows:
                email = row[0] or 'N/A'
                name = row[1] or 'N/A'
                phone = row[2] or 'N/A'
                ticket_id = row[4] or 'N/A'
                registered = 'Yes' if row[3] == 1 else 'No'
                verified = 'Yes' if row[5] == 1 else 'No'
                
                print(f"{email[:29]:<30} {name[:19]:<20} {phone[:17]:<18} {ticket_id[:11]:<12} {registered:<12} {verified:<12}")
        else:
            print("[WARNING] No users found in database!")
        
        conn.close()
        
    except Exception as e:
        print(f"[ERROR] Error reading database: {e}")
        conn.close()

if __name__ == "__main__":
    print("=" * 100)
    print("DATABASE CHECK AND RECOVERY TOOL")
    print("=" * 100)
    print()
    check_database()
    print()
    print("=" * 100)
    print("To recover data, check the 'database_backups' folder for backup files.")
    print("=" * 100)

