
from utils.database import init_database
from utils.security import get_security_key_from_image
from interface.animations import opening_animation
from core.user import User
import sqlite3
from utils.database import DB_PATH

def create_user():
    print("\n🧍 New user detected!")
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    print("\n🔒 Now, choose an image file to generate your security key...")
    try:
        key = get_security_key_from_image()
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    user_id = f"{first_name.lower()}_{last_name.lower()}"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO users (user_id, first_name, last_name, key) VALUES (?, ?, ?, ?)',
              (user_id, first_name, last_name, key))
    c.execute('INSERT INTO balance (user_id, current_balance) VALUES (?, 0)', (user_id,))
    conn.commit()
    conn.close()
    return User(user_id=user_id, first_name=first_name, last_name=last_name, key=key)

def get_existing_user():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT user_id, first_name, last_name, key FROM users')
    users = c.fetchall()
    conn.close()
    if not users:
        return None
    print("\n👥 Existing users:")
    for i, u in enumerate(users):
        print(f"[{i + 1}] {u[1]} {u[2]}")
    try:
        choice = int(input("\nSelect user by number: ").strip())
        user_row = users[choice - 1]
        return User(*user_row)
    except:
        return None

def init_app_session():
    opening_animation()
    init_database()
    user = get_existing_user()
    if not user:
        user = create_user()
    return user
