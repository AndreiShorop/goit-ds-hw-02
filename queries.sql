-- 1. Отримати всі завдання певного користувача (наприклад, user_id = 1)
SELECT * FROM tasks WHERE user_id = 1;

-- 2. Вибрати завдання зі статусом 'new'
SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3. Оновити статус конкретного завдання
UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 1;

-- 4. Користувачі, які не мають жодного завдання
SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);

-- 5. Додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, status_id, user_id) 
VALUES ('New Task Title', 'Description text', (SELECT id FROM status WHERE name = 'new'), 1);

-- 6. Отримати незавершені завдання
SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');

-- 7. Видалити завдання
DELETE FROM tasks WHERE id = 1;

-- 8. Знайти користувачів за email
SELECT * FROM users WHERE email LIKE '%@example.com';

-- 9. Оновити ім'я користувача
UPDATE users SET fullname = 'Ivan Ivanov' WHERE id = 1;

-- 10. Кількість завдань для кожного статусу
SELECT s.name, COUNT(t.id) as total 
FROM status s 
LEFT JOIN tasks t ON s.id = t.status_id 
GROUP BY s.name;

-- 11. Завдання користувачів з певним доменом пошти (@example.com)
SELECT t.* FROM tasks t 
JOIN users u ON t.user_id = u.id 
WHERE u.email LIKE '%@example.com';

-- 12. Завдання без опису
SELECT * FROM tasks WHERE description IS NULL OR description = '';

-- 13. Користувачі та завдання у статусі 'in progress'
SELECT u.fullname, t.title 
FROM users u 
INNER JOIN tasks t ON u.id = t.user_id 
INNER JOIN status s ON t.status_id = s.id 
WHERE s.name = 'in progress';

-- 14. Користувачі та кількість їхніх завдань
SELECT u.fullname, COUNT(t.id) as task_count 
FROM users u 
LEFT JOIN tasks t ON u.id = t.user_id 
GROUP BY u.id;