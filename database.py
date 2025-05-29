import psycopg2
import os

DB_URL = os.environ.get("DATABASE_URL")  # Render 會自動幫你設這個環境變數

def get_connection():
    return psycopg2.connect(DB_URL)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservations (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT,
                    start_location TEXT,
                    end_location TEXT,
                    datetime TEXT,
                    is_shared BOOLEAN,
                    payment TEXT,
                    group_id TEXT,
                    status TEXT DEFAULT 'active'
                )
            ''')
            conn.commit()

def add_reservation(data):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO reservations (user_id, start_location, end_location, datetime, is_shared, payment)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', data)
            conn.commit()

def cancel_reservation(user_id):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('UPDATE reservations SET status = %s WHERE user_id = %s AND status = %s', ('cancelled', user_id, 'active'))
            conn.commit()

def get_active_reservations():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM reservations WHERE status = %s', ('active',))
            return cursor.fetchall()

def assign_group(user_ids, group_id, shared_price):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            for user_id in user_ids:
                cursor.execute('UPDATE reservations SET group_id = %s, payment = %s WHERE user_id = %s', (group_id, shared_price, user_id))
        conn.commit()
