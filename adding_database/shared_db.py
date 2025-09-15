# shared_db.py
import sqlite3

db_file = "diary_app.db"

def init_db():
    
    '''Initialize all tables for the app if they don't exist.'''
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        #Users table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        #Diaries table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                image TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        #Diary entries table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diary_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diary_id INTEGER NOT NULL,
                entry_date TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY(diary_id) REFERENCES diaries(id)
            )
        """)
        #Questionnaire table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questionnaire (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                answer TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        #Responses table for questionnaire
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question_number INTEGER NOT NULL,
                response TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        conn.commit()


class DatabaseManager:
    def __init__(self, db_name="diary_app.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        import sqlite3
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    question_number INTEGER NOT NULL,
                    response TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            conn.commit()

    def register_user(self, username, password):
        import sqlite3
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()

    def validate_user(self, username, password):
        import sqlite3
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username FROM users WHERE username=? AND password=?", (username, password))
            return cursor.fetchone()

    def save_response(self, user_id, question_number, response_text):
        import sqlite3
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO responses (user_id, question_number, response) VALUES (?, ?, ?)",
                           (user_id, question_number, response_text))
            conn.commit()


    #---- Questionnaire functions ----
    def save_response(self, user_id, question_number, response_text):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO responses (user_id, question_number, response) VALUES (?, ?, ?)",
                (user_id, question_number, response_text)
            )
            conn.commit()

    def get_user_responses(self, user_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT question_number, response FROM responses WHERE user_id=?",
                (user_id,)
            )
            return cursor.fetchall()
