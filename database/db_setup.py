import sqlite3


def initialize_db():
    conn = sqlite3.connect('maintenance.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS machines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        type TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS maintenance_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        machine_id INTEGER NOT NULL,
        maintenance_type TEXT NOT NULL,
        date_scheduled TIMESTAMP NOT NULL,
        technician_name TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (machine_id) REFERENCES machines (id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS maintenance_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        completion_date TIMESTAMP NOT NULL,
        remarks TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES maintenance_tasks (id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES ('admin', 'admin123', 'Administrator')
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()
