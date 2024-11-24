from faker import Faker
import psycopg2
import random

fake = Faker()

connection = psycopg2.connect(
    dbname="task_management",
    user="Luxeon",
    password="1q2w3e4r5",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

cursor.execute("""
INSERT INTO status (name) VALUES 
('new'), 
('in progress'), 
('completed')
ON CONFLICT (name) DO NOTHING;
""")

for _ in range(10):
    fullname = fake.name()
    email = fake.unique.email()
    cursor.execute("""
    INSERT INTO users (fullname, email) 
    VALUES (%s, %s) 
    ON CONFLICT (email) DO NOTHING;
    """, (fullname, email))

cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM status")
status_ids = [row[0] for row in cursor.fetchall()]

for _ in range(50):
    title = fake.sentence(nb_words=6)
    description = fake.text(max_nb_chars=200) if random.choice([True, False]) else None
    status_id = random.choice(status_ids)
    user_id = random.choice(user_ids)
    cursor.execute("""
    INSERT INTO tasks (title, description, status_id, user_id) 
    VALUES (%s, %s, %s, %s);
    """, (title, description, status_id, user_id))

connection.commit()

cursor.close()
connection.close()

print("Таблиці успішно наповнені!")