"""
PostgreSQL Database Handler
Uses connection pooling and graceful reconnection for production stability

PRODUCTION: Requires Python 3.11.9 (set in runtime.txt) for psycopg2-binary compatibility
"""

import os
from datetime import datetime
import time

# PRODUCTION FIX: Import psycopg2 with clear error handling for Python version compatibility
try:
    import psycopg2
    from psycopg2 import pool, sql
    from psycopg2.extras import RealDictCursor
except ImportError as e:
    print(f"❌ CRITICAL: Failed to import psycopg2: {e}")
    print("❌ This usually means Python version is incompatible (need Python 3.11.9)")
    print("❌ Check runtime.txt is set to: python-3.11.9")
    raise ImportError(
        "psycopg2-binary requires Python 3.11.9. "
        "Set runtime.txt to 'python-3.11.9' and redeploy."
    ) from e

# Get DATABASE_URL from environment (required for Render PostgreSQL)
DATABASE_URL = os.getenv('DATABASE_URL')

# Connection pool for production
_connection_pool = None

def get_connection_pool():
    """Get or create connection pool - singleton pattern"""
    global _connection_pool
    if _connection_pool is None:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required. Set it in Render dashboard.")
        
        try:
            # Parse DATABASE_URL and create connection pool
            # Pool size: min 1, max 5 connections
            _connection_pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=5,
                dsn=DATABASE_URL
            )
            print("✅ PostgreSQL connection pool created")
        except Exception as e:
            print(f"❌ Error creating connection pool: {e}")
            raise
    return _connection_pool

def get_connection():
    """Get a connection from the pool with retry logic"""
    pool = get_connection_pool()
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            conn = pool.getconn()
            # Test connection
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
            return conn
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            print(f"⚠️ Connection error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise
    return None

def return_connection(conn):
    """Return connection to pool"""
    if conn and _connection_pool:
        try:
            _connection_pool.putconn(conn)
        except Exception as e:
            print(f"⚠️ Error returning connection to pool: {e}")

def init_db():
    """Initialize database - create table if it doesn't exist (DO NOT recreate on every restart)"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # Create table only if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS allowed (
                    email VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(255),
                    phone VARCHAR(50),
                    registered INTEGER DEFAULT 0,
                    ticket_id VARCHAR(50),
                    verified INTEGER DEFAULT 0,
                    created_at TIMESTAMP,
                    registered_at TIMESTAMP,
                    verified_at TIMESTAMP
                )
            """)
            
            # Add missing columns if they don't exist (for existing databases)
            # PostgreSQL doesn't support IF NOT EXISTS for ALTER TABLE, so we check first
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='allowed' AND column_name='created_at'
            """)
            if not cur.fetchone():
                cur.execute("ALTER TABLE allowed ADD COLUMN created_at TIMESTAMP")
            
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='allowed' AND column_name='registered_at'
            """)
            if not cur.fetchone():
                cur.execute("ALTER TABLE allowed ADD COLUMN registered_at TIMESTAMP")
            
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='allowed' AND column_name='verified_at'
            """)
            if not cur.fetchone():
                cur.execute("ALTER TABLE allowed ADD COLUMN verified_at TIMESTAMP")
            
            # Add money_amount column if it doesn't exist
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='allowed' AND column_name='money_amount'
            """)
            if not cur.fetchone():
                cur.execute("ALTER TABLE allowed ADD COLUMN money_amount DECIMAL(10, 2) DEFAULT 0")
            
            conn.commit()
            print("✅ Database initialized (table exists or created)")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Error initializing database: {e}")
        raise
    finally:
        if conn:
            return_connection(conn)

def get_user(email=None, ticket_id=None):
    """Get user by email or ticket_id"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if email:
                cur.execute("SELECT * FROM allowed WHERE email = %s", (email,))
            elif ticket_id:
                cur.execute("SELECT * FROM allowed WHERE ticket_id = %s", (ticket_id,))
            else:
                return None
            
            row = cur.fetchone()
            if row:
                # Convert to regular dict and handle timestamp conversion
                result = dict(row)
                # Convert timestamps to ISO format strings for compatibility
                for key in ['created_at', 'registered_at', 'verified_at']:
                    if result.get(key) and hasattr(result[key], 'isoformat'):
                        result[key] = result[key].isoformat()
                return result
            return None
    except Exception as e:
        print(f"❌ Error getting user: {e}")
        return None
    finally:
        if conn:
            return_connection(conn)

def add_user(email):
    """Add a new user"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            now = datetime.now()
            cur.execute(
                "INSERT INTO allowed (email, created_at) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                (email, now)
            )
            conn.commit()
            print(f"✅ User added: {email}")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Error adding user: {e}")
        raise
    finally:
        if conn:
            return_connection(conn)

def update_user(email, **kwargs):
    """Update user fields"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # Build dynamic UPDATE query
            updates = []
            values = []
            for key, value in kwargs.items():
                # Convert ISO format strings to datetime for timestamp fields
                if key in ['created_at', 'registered_at', 'verified_at'] and isinstance(value, str):
                    try:
                        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    except:
                        pass
                updates.append(f"{key} = %s")
                values.append(value)
            
            if updates:
                values.append(email)
                query = f"UPDATE allowed SET {', '.join(updates)} WHERE email = %s"
                cur.execute(query, values)
                conn.commit()
                print(f"✅ User updated: {email}")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Error updating user: {e}")
        raise
    finally:
        if conn:
            return_connection(conn)

def fetch_all_users():
    """Fetch ALL users from database - NO LIMIT, supports up to 150+ users"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT email, name, phone, registered, ticket_id, verified, 
                       created_at, registered_at, verified_at, money_amount
                FROM allowed 
                ORDER BY created_at DESC NULLS LAST, email ASC
            """)
            rows = cur.fetchall()
            # Convert to list of tuples for compatibility with existing template code
            # Template expects: (email, name, phone, registered, ticket_id, verified, created_at, registered_at, verified_at, money_amount)
            result = []
            for row in rows:
                # Convert timestamps to strings for template compatibility
                result.append((
                    row[0],  # email
                    row[1],  # name
                    row[2],  # phone
                    row[3],  # registered
                    row[4],  # ticket_id
                    row[5],  # verified
                    row[6].isoformat() if row[6] else None,  # created_at
                    row[7].isoformat() if row[7] else None,  # registered_at
                    row[8].isoformat() if row[8] else None,  # verified_at
                    float(row[9]) if row[9] is not None else 0.0  # money_amount
                ))
            return result
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        return []
    finally:
        if conn:
            return_connection(conn)

def delete_user(email):
    """Delete a user from the database by email"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM allowed WHERE email = %s", (email,))
            deleted = cur.rowcount > 0
            conn.commit()
            if deleted:
                print(f"✅ User deleted: {email}")
            return deleted
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"❌ Error deleting user: {e}")
        return False
    finally:
        if conn:
            return_connection(conn)

def get_stats():
    """Get database statistics"""
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM allowed")
            total = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM allowed WHERE registered = 1")
            registered = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM allowed WHERE verified = 1")
            verified = cur.fetchone()[0]
            
            pending = total - registered
            
            return {
                "total": total,
                "registered": registered,
                "verified": verified,
                "pending": pending
            }
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return {
            "total": 0,
            "registered": 0,
            "verified": 0,
            "pending": 0
        }
    finally:
        if conn:
            return_connection(conn)

def close_pool():
    """Close all connections in pool (for graceful shutdown)"""
    global _connection_pool
    if _connection_pool:
        _connection_pool.closeall()
        _connection_pool = None
        print("✅ Connection pool closed")
