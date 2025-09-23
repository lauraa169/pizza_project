import sqlite3

# Database file
DB_NAME = "pizza_system.db"

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

# Step 4: test query
cursor.execute('')
rows = cursor.fetchall()

print("\n📋 Customers in database:")
for row in rows:
    print(f"- {row[0]} ({row[1]})")

# Close connection
conn.commit()
conn.close()
print("\n🎉 Setup complete!")
