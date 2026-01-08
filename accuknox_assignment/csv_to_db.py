import csv
import sqlite3

def migrate_csv_to_db(csv_file_path):
    # Connect to the database (creates it if it doesn't exist)
    db_conn = sqlite3.connect("users_data.db")
    cursor = db_conn.cursor()

    try:
        # 1. Setup the table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')

        # 2. Open and process the CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            inserted_count = 0
            skipped_count = 0

            for row in reader:
                name = row.get('name')
                email = row.get('email')

                if name and email:
                    try:
                        cursor.execute(
                            "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", 
                            (name.strip(), email.strip())
                        )
                        if cursor.rowcount > 0:
                            inserted_count += 1
                            print(f"Inserted: {name} ({email})")
                        else:
                            skipped_count += 1
                            print(f"Skipped (duplicate): {name} ({email})")
                    except sqlite3.Error as e:
                        print(f"Error inserting {name}: {e}")
                else:
                    skipped_count += 1
                    print(f"Skipped (missing data): {row}")

        # 3. Commit changes
        db_conn.commit()

        # 4. Summary
        print(f"\nMigration complete. Added: {inserted_count}, Skipped/Duplicates: {skipped_count}\n")

        # 5. Show all rows currently in the database
        print("Current users in database:")
        cursor.execute("SELECT * FROM users")
        all_rows = cursor.fetchall()
        for r in all_rows:
            print(r)

    except Exception as e:
        print(f"An error occurred: {e}")
        db_conn.rollback()
    
    finally:
        cursor.close()
        db_conn.close()


if __name__ == "__main__":
    migrate_csv_to_db("users.csv")
