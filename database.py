import sqlite3
import json

def init_db():
    try:
        conn = sqlite3.connect('settings.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                chat_id INTEGER PRIMARY KEY,
                settings TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        conn.close()

def save_settings(chat_id, settings):
    try:
        conn = sqlite3.connect('settings.db')
        cursor = conn.cursor()
        cursor.execute('REPLACE INTO user_settings (chat_id, settings) VALUES (?, ?)', (chat_id, json.dumps(settings)))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при сохранении настроек: {e}")
    finally:
        conn.close()

def get_settings(chat_id):
    try:
        conn = sqlite3.connect('settings.db')
        cursor = conn.cursor()
        cursor.execute('SELECT settings FROM user_settings WHERE chat_id=?', (chat_id,))
        row = cursor.fetchone()
        return json.loads(row[0]) if row else {"volume_threshold": 50, "oi_threshold": 5}
    except sqlite3.Error as e:
        print(f"Ошибка при получении настроек: {e}")
        return {"volume_threshold": 50, "oi_threshold": 5}
    finally:
        conn.close()
