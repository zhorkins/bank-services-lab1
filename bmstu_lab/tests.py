from django.test import TestCase

# Create your tests here.
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    user="student",
    password="student",
    dbname="student"
)
cursor = conn.cursor()

# Вставляем новую книгу (id назначится автоматически)
cursor.execute(
    "INSERT INTO books (name, description) VALUES (%s, %s);",
    ("Преступление и наказание", "Роман Ф.М. Достоевского")
)
conn.commit()
print("Книга добавлена!")

# Проверим, что получилось
cursor.execute("SELECT * FROM books;")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.close()
conn.close()