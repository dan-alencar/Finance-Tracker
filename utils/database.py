import sqlite3
import os

# Get project root: finance_app/../..
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DB_DIR, 'finance.db')
print(DB_PATH)

def has_users():
    """Returns True if there's at least one user in the DB."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        count = c.fetchone()[0]
        return count > 0


def is_database_initialized():
    """Check if 'users' table exists to confirm DB is valid."""
    if not os.path.exists(DB_PATH):
        return False

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        return c.fetchone() is not None


def init_database():
    if not os.path.exists(DB_PATH):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            key TEXT NOT NULL
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS balance (
            user_id TEXT PRIMARY KEY,
            current_balance REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')

    conn.commit()
    conn.close()

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()

        # Users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                security_hash TEXT NOT NULL
            )
        ''')

        # Balance table
        c.execute('''
            CREATE TABLE IF NOT EXISTS balance (
                user_id TEXT PRIMARY KEY,
                current_balance REAL NOT NULL DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        # Income sources
        c.execute('''
            CREATE TABLE IF NOT EXISTS income (
                income_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                source TEXT,
                amount REAL NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        # Installments
        c.execute('''
            CREATE TABLE IF NOT EXISTS installments (
                installment_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                description TEXT,
                total_value REAL,
                monthly_value REAL,
                months_remaining INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        conn.commit()

# === User Functions ===
def is_first_time_user():
    return not (os.path.exists(DB_PATH)) or os.stat(DB_PATH).st_size == 0

def insert_user(user):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?)',
                  (user.user_id, user.first_name, user.last_name, user.security_hash))
        c.execute('INSERT INTO balance (user_id, current_balance) VALUES (?, ?)',
                  (user.user_id, 0.0))
        conn.commit()

def get_all_users():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users')
        return c.fetchall()

def get_user_by_hash(security_hash):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE security_hash = ?', (security_hash,))
        return c.fetchone()

# === Balance Functions ===
def get_balance(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT current_balance FROM balance WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        return row[0] if row else 0.0

def set_balance(user_id, value):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE balance SET current_balance = ? WHERE user_id = ?', (value, user_id))
        conn.commit()

def add_to_balance(user_id, value):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE balance SET current_balance = current_balance + ? WHERE user_id = ?', (value, user_id))
        conn.commit()

def subtract_from_balance(user_id, value):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE balance SET current_balance = current_balance - ? WHERE user_id = ?', (value, user_id))
        conn.commit()
