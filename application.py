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

def slect():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Example: list all pizzas
    cursor.execute("SELECT * FROM Pizza;")
    rows = cursor.fetchall()  # fetch all results

    print("✅ Pizzas in the database:")
    for row in rows:
        print(row)  # prints each row as a tuple

    # Example: list all customers
    cursor.execute("SELECT * FROM Customer;")
    customers = cursor.fetchall()
    print("\n✅ Customers in the database:")
    for customer in customers:
        print(customer)

    conn.close()

slect()
