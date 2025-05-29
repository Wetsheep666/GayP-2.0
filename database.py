import sqlite3

conn = sqlite3.connect('carpool.db', check_same_thread=False)
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

def add_reservation(data):
    cursor.execute('''
        INSERT INTO reservations (user_id, start_location, end_location, datetime, is_shared, payment)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()

def cancel_reservation(user_id):
    cursor.execute('UPDATE reservations SET status = "cancelled" WHERE user_id = ? AND status = "active"', (user_id,))
    conn.commit()

def get_active_reservations():
    cursor.execute('SELECT * FROM reservations WHERE status = "active"')
    return cursor.fetchall()

def assign_group(user_ids, group_id, shared_price):
    for user_id in user_ids:
        cursor.execute('UPDATE reservations SET group_id = ?, payment = ? WHERE user_id = ?', (group_id, shared_price, user_id))
    conn.commit()
