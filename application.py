import sqlite3

# Database file
DB_NAME = "identifier.sqlite"

def setup():
    # Step 1: connect (creates DB if not exists)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Step 2: load and execute schema
    with open("Pizza_test.sql", "r") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    print("✅ Schema created successfully.")

    # Step 3: load and execute data inserts
    with open("data.sql", "r") as f:
        data_sql = f.read()
    cursor.executescript(data_sql)
    print("✅ Data inserted successfully.")

setup()
