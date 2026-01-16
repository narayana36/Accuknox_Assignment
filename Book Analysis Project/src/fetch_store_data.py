import requests
import mysql.connector

# Database Connection Details
db_config = {
    'host': 'localhost',      # Change if using a remote server
    'user': 'root',           # MySQL username
    'password': 'paswrd', # password
    'database': 'bookslist'  # Ensure this database exists first
}

# --------- API URL (REST API) ---------
API_URL = "https://openlibrary.org/search.json?subject=fiction"

# --------- Step 1: Call REST API ----------
response = requests.get(API_URL)
data = response.json()
docs = data.get("docs", [])

# --------- Step 2: MySQL Connection --------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="paswrd",
    database="bookslist"     
)

cursor = conn.cursor()

# --------- Step 3: Insert Into Existing Table ---------
insert_query = """
INSERT INTO books (title, author, year)
VALUES (%s, %s, %s)
"""

for book in docs:
    title = book.get("title", "Unknown")
    authors = book.get("author_name", [])
    author = authors[0] if authors else "Unknown"
    year = book.get("first_publish_year", None)

    cursor.execute(insert_query, (title, author, year))

conn.commit()

# --------- Step 4: Display Data -------------
cursor.execute("SELECT title, author, year FROM books LIMIT 10")
rows = cursor.fetchall()

print("\nStored Books (First 10):\n")
for row in rows:
    print(f"Title: {row[0]} | Author: {row[1]} | Year: {row[2]}")

cursor.close()
conn.close()
