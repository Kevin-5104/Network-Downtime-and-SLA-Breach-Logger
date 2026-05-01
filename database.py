import sqlite3

class Database:
    def __init__(self, db_name="sla_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS downtime_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_name TEXT,
                ip TEXT,
                down_time TEXT,
                up_time TEXT,
                duration_seconds REAL
            )
        ''')
        self.conn.commit()

    def log_downtime(self, device_name, ip, down_time, up_time, duration_seconds):
        self.cursor.execute('''
            INSERT INTO downtime_log (device_name, ip, down_time, up_time, duration_seconds)
            VALUES (?, ?, ?, ?, ?)
        ''', (device_name, ip, down_time, up_time, duration_seconds))
        self.conn.commit()

    def get_all_logs(self):
        self.cursor.execute('SELECT * FROM downtime_log')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()