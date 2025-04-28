import sqlite3

def init_db():
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            chat_id INTEGER PRIMARY KEY,
            settings TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_settings(chat_id, settings):
    import json
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute('REPLACE INTO user_settings (chat_id, settings) VALUES (?, ?)', (chat_id, json.dumps(settings)))
    conn.commit()
    conn.close()

def get_settings(chat_id):
    import json
    conn = sqlite3.connect('settings.db')
    cursor = conn.cursor()
    cursor.execute('SELECT settings FROM user_settings WHERE chat_id=?', (chat_id,))
    row = cursor.fetchone()
    conn.close()
    return json.loads(row[0]) if row else None