import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self):
        self.db_path = "data/astronomy.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize database with required tables"""
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_data TEXT NOT NULL,
                location TEXT NOT NULL,
                event_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_id INTEGER,
                alert_sent BOOLEAN DEFAULT FALSE,
                sent_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_user_preferences(self, username, preferences):
        """Save user preferences to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET preferences = ? WHERE username = ?
        ''', (json.dumps(preferences), username))
        
        conn.commit()
        conn.close()
    
    def get_user_preferences(self, username):
        """Get user preferences from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT preferences FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0]:
            return json.loads(result[0])
        return {}
    
    def log_event(self, event_type, event_data, location, event_time=None):
        """Log an astronomical event to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO events (event_type, event_data, location, event_time)
            VALUES (?, ?, ?, ?)
        ''', (event_type, json.dumps(event_data), location, event_time or datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_recent_events(self, limit=50):
        """Get recent events from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT event_type, event_data, location, event_time 
            FROM events 
            ORDER BY event_time DESC 
            LIMIT ?
        ''', (limit,))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'type': row[0],
                'data': json.loads(row[1]),
                'location': row[2],
                'time': row[3]
            })
        
        conn.close()
        return events

# Global database instance
db_manager = DatabaseManager()