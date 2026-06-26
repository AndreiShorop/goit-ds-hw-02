import sqlite3
from faker import Faker  # Змінено тут
import random

fake = Faker()


def seed_db():
    with sqlite3.connect('data.db') as conn:
        cur = conn.cursor()

        statuses = [('new',), ('in progress',), ('completed',)]
        cur.executemany("INSERT OR IGNORE INTO status (name) VALUES (?);", statuses)

        users = []
        for _ in range(10):
            users.append((fake.name(), fake.unique.email()))
        cur.executemany("INSERT INTO users (fullname, email) VALUES (?, ?);", users)

        cur.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cur.fetchall()]
        
        cur.execute("SELECT id FROM status")
        status_ids = [row[0] for row in cur.fetchall()]

       
        tasks = []
        for _ in range(20):
            tasks.append((
                fake.sentence(nb_words=4),
                fake.text(max_nb_chars=200),
                random.choice(status_ids),
                random.choice(user_ids)
            ))
        cur.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?);", tasks)

        conn.commit()
        print("База даних успішно заповнена випадковими даними.")

if __name__ == "__main__":
    seed_db()