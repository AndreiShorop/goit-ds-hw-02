import sqlite3

def execute_query(sql, params=()):
    with sqlite3.connect('data.db') as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON;")
        cur.execute(sql, params)
        if sql.strip().upper().startswith("SELECT"):
            return cur.fetchall()
        conn.commit()

print("1. Завдання користувача з id=2:")
print(execute_query("SELECT * FROM tasks WHERE user_id = 1;"))

print("\n2. Завдання зі статусом 'new' (підзапит):")
print(execute_query("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');"))

print("\n3. Оновлення статусу завдання id=2 на 'in progress':")
execute_query("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 2;")
print("Оновлено.")

print("\n4. Користувачі без завдань:")
print(execute_query("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);"))

print("\n5. Додавання нового завдання для першого наявного користувача:")
user_data = execute_query("SELECT id FROM users LIMIT 1;")
if user_data:
    actual_user_id = user_data[0][0]
    execute_query("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?);", 
                  ('Test Task', 'Doing homework', 1, actual_user_id))
    print(f"Додано завдання для користувача id={actual_user_id}")
else:
    print("Помилка: в базі немає жодного користувача!")

print("\n6. Незавершені завдання (не 'completed'):")
print(execute_query("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');"))

print("\n7. Видалення завдання id=3:")
execute_query("DELETE FROM tasks WHERE id = 3;")
print("Видалено.")

print("\n8. Користувачі з поштою @example.com:")
print(execute_query("SELECT * FROM users WHERE email LIKE '%@example.com';"))

print("\n9. Оновлення імені користувача id=1:")
execute_query("UPDATE users SET fullname = 'New Name' WHERE id = 1;")
print("Оновлено.")

print("\n10. Кількість завдань для кожного статусу:")
print(execute_query("SELECT s.name, COUNT(t.id) FROM status s LEFT JOIN tasks t ON s.id = t.status_id GROUP BY s.name;"))

print("\n11. Завдання користувачів з доменом @example.net:")
print(execute_query("""
    SELECT t.* FROM tasks t 
    JOIN users u ON t.user_id = u.id 
    WHERE u.email LIKE '%@example.net';
"""))

print("\n12. Завдання без опису:")
print(execute_query("SELECT * FROM tasks WHERE description IS NULL OR description = '';"))

print("\n13. Користувачі та їхні завдання у статусі 'in progress':")
print(execute_query("""
    SELECT u.fullname, t.title FROM users u 
    INNER JOIN tasks t ON u.id = t.user_id 
    INNER JOIN status s ON t.status_id = s.id 
    WHERE s.name = 'in progress';
"""))

print("\n14. Користувачі та кількість їхніх завдань:")
print(execute_query("""
    SELECT u.fullname, COUNT(t.id) FROM users u 
    LEFT JOIN tasks t ON u.id = t.user_id 
    GROUP BY u.id;
"""))