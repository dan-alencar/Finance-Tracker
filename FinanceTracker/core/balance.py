import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_DIR = os.path.join(BASE_DIR, 'db')
DB_PATH = os.path.join(DB_DIR, 'finance.db')

os.makedirs(DB_DIR, exist_ok=True)

def format_brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def get_balance(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT current_balance FROM balance WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        return row[0] if row else 0.0

def set_balance(user_id, value):
    if value < 0:
        raise ValueError("O saldo não pode ser negativo.")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE balance SET current_balance = ? WHERE user_id = ?', (value, user_id))
        conn.commit()

def add_to_balance(user_id, value):
    if value < 0:
        raise ValueError("Use subtração para valores negativos.")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE balance SET current_balance = current_balance + ? WHERE user_id = ?', (value, user_id))
        conn.commit()

def subtract_from_balance(user_id, value):
    if value < 0:
        raise ValueError("Use adição para valores negativos.")
    current = get_balance(user_id)
    if value > current:
        raise ValueError("Saldo insuficiente.")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE balance SET current_balance = current_balance - ? WHERE user_id = ?', (value, user_id))
        conn.commit()

