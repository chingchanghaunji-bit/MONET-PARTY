"""
Database Backup and Recovery Module
Provides automatic backup and recovery functionality for the database
"""

import sqlite3
import os
import shutil
from datetime import datetime

DB_PATH = 'database.db'
BACKUP_DIR = 'database_backups'

def ensure_backup_dir():
    """Create backup directory if it doesn't exist"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def create_backup():
    """Create a timestamped backup of the database"""
    ensure_backup_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'database_backup_{timestamp}.db'
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    if os.path.exists(DB_PATH):
        try:
            shutil.copy2(DB_PATH, backup_path)
            print(f"✅ Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return None
    else:
        print("⚠️ Database file not found, cannot create backup")
        return None

def list_backups():
    """List all available backups"""
    ensure_backup_dir()
    backups = []
    if os.path.exists(BACKUP_DIR):
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith('database_backup_') and filename.endswith('.db'):
                filepath = os.path.join(BACKUP_DIR, filename)
                backups.append({
                    'filename': filename,
                    'path': filepath,
                    'timestamp': os.path.getmtime(filepath),
                    'size': os.path.getsize(filepath)
                })
        # Sort by timestamp (newest first)
        backups.sort(key=lambda x: x['timestamp'], reverse=True)
    return backups

def restore_backup(backup_path):
    """Restore database from a backup file"""
    if not os.path.exists(backup_path):
        return False, "Backup file not found"
    
    try:
        # Create backup of current database before restoring
        if os.path.exists(DB_PATH):
            current_backup = f"{DB_PATH}.before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(DB_PATH, current_backup)
        
        # Restore from backup
        shutil.copy2(backup_path, DB_PATH)
        return True, "Database restored successfully"
    except Exception as e:
        return False, f"Error restoring backup: {e}"

def get_database_info():
    """Get information about the current database"""
    if not os.path.exists(DB_PATH):
        return None
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # Get total count
        total = c.execute("SELECT COUNT(*) FROM allowed").fetchone()[0]
        
        # Get registered count
        registered = c.execute("SELECT COUNT(*) FROM allowed WHERE registered=1").fetchone()[0]
        
        # Get verified count
        verified = c.execute("SELECT COUNT(*) FROM allowed WHERE verified=1").fetchone()[0]
        
        # Get recent registrations
        recent = c.execute("""
            SELECT email, name, registered_at 
            FROM allowed 
            WHERE registered=1 
            ORDER BY registered_at DESC 
            LIMIT 10
        """).fetchall()
        
        # Get database file size
        file_size = os.path.getsize(DB_PATH)
        file_modified = os.path.getmtime(DB_PATH)
        
        conn.close()
        
        return {
            'total': total,
            'registered': registered,
            'verified': verified,
            'recent': recent,
            'file_size': file_size,
            'file_modified': datetime.fromtimestamp(file_modified).isoformat()
        }
    except Exception as e:
        conn.close()
        return {'error': str(e)}

