import sqlite3

def create_db():
    
    with sqlite3.connect('data.db') as conn:
        cur = conn.cursor()

       
        cur.execute("PRAGMA foreign_keys = ON;")

        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname VARCHAR(100),
                email VARCHAR(100) UNIQUE
            );
        """)

        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) UNIQUE
            );
        """)

       
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(100),
                description TEXT,
                status_id INTEGER,
                user_id INTEGER,
                FOREIGN KEY (status_id) REFERENCES status (id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)
        
        conn.commit()
        print("База даних та таблиці успішно створені.")

if __name__ == "__main__":
    create_db()