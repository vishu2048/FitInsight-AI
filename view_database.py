
import sqlite3
from pathlib import Path

# Find database files in the project
project_path = Path(__file__).resolve().parent

database_files = list(project_path.rglob("*.db"))

if not database_files:
    print("No database file found!")
    exit()

print("Available databases:")

for i, file in enumerate(database_files):
    print(f"{i + 1}. {file}")

# Select the first database
db_path = database_files[0]

print(f"\nConnected to: {db_path}")

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Display all tables
cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table'
""")

tables = cursor.fetchall()

for table in tables:

    table_name = table[0]

    print("\n" + "=" * 50)
    print("TABLE:", table_name)
    print("=" * 50)

    cursor.execute(f'SELECT * FROM "{table_name}"')

    rows = cursor.fetchall()

    columns = [
        description[0]
        for description in cursor.description
    ]

    print("Columns:", columns)

    for row in rows:
        print(row)

    print("Total entries:", len(rows))

connection.close()
