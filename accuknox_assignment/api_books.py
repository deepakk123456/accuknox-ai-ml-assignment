import requests
import sqlite3

def get_library_data():
    url = "https://openlibrary.org/subjects/scifi.json?limit=10"
    headers = {'User-Agent': 'BookTracker/1.0'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        books = resp.json().get('works', [])
        print(f"Fetched {len(books)} books from API.")  # debug print
        if not books:
            print("API returned no books, using fallback data.")
        return books
    except Exception as e:
        print(f"Failed to fetch data from API: {e}")
        print("Using fallback mock data.")
        # Mock fallback data
        return [
            {"title": "Dune", "authors": [{"name": "Frank Herbert"}], "first_publish_year": 1965},
            {"title": "Neuromancer", "authors": [{"name": "William Gibson"}], "first_publish_year": 1984},
            {"title": "Foundation", "authors": [{"name": "Isaac Asimov"}], "first_publish_year": 1951},
        ]

def init_db():
    conn = sqlite3.connect("books_cache.db")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            pub_year INTEGER,
            UNIQUE(title, author)
        )
    ''')
    return conn

def save_to_db(connection, book_list):
    cursor = connection.cursor()
    inserted_count = 0
    
    for book in book_list:
        title = book.get('title')
        authors = book.get('authors', [])
        author_name = authors[0].get('name') if authors else "Unknown"
        year = book.get('first_publish_year', 0)

        try:
            sql = "INSERT OR IGNORE INTO books (title, author, pub_year) VALUES (?, ?, ?)"
            cursor.execute(sql, (title, author_name, year))
            if cursor.rowcount > 0:
                inserted_count += 1
        except sqlite3.Error as e:
            print(f"Database error on '{title}': {e}")
    
    connection.commit()
    cursor.close()
    print(f"Done. Added {inserted_count} new unique books.")

def run_pipeline():
    data = get_library_data()
    if not data:
        print("No data to process.")
        return

    db_conn = init_db()
    save_to_db(db_conn, data)

    print("\n--- Latest 5 Entries ---")
    rows = db_conn.execute("SELECT * FROM books ORDER BY id DESC LIMIT 5").fetchall()
    for row in rows:
        print(f"ID: {row[0]} | {row[1]} by {row[2]} ({row[3]})")

    db_conn.close()

if __name__ == "__main__":
    run_pipeline()
