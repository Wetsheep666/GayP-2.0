import sqlite3

DB_NAME = 'carpool.db'

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        start_location TEXT,
        end_location TEXT,
        datetime TEXT,
        is_shared INTEGER,
        payment TEXT,
        group_id TEXT,
        status TEXT DEFAULT 'active'
    )
    ''')
    conn.commit()
    conn.close()

def add_reservation(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reservations (user_id, start_location, end_location, datetime, is_shared, payment)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()

def cancel_reservation(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE reservations SET status = "cancelled" WHERE user_id = ? AND status = "active"', (user_id,))
    conn.commit()
    conn.close()

def get_active_reservations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reservations WHERE status = "active"')
    results = cursor.fetchall()
    conn.close()
    return results

def assign_group(user_ids, group_id, shared_price):
    conn = get_connection()
    cursor = conn.cursor()
    for user_id in user_ids:
        cursor.execute('UPDATE reservations SET group_id = ?, payment = ? WHERE user_id = ?', (group_id, shared_price, user_id))
    conn.commit()
    conn.close()
