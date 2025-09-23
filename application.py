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
cursor.execute('''SELECT 
    o.Order_ID,
    c.Customer_Name,
    c.Customer_Surname,
    s.Name AS Staff_FirstName,
    s.Surname AS Staff_LastName,
    p.Pizza_Name,
    op.Quantity,
    d.Drink_Name,
    ds.Dessert_Name,
    dis.Percent AS DiscountPercent,
    o.Order_Price,
    o.Delivered,
    o.Order_Time
FROM Order o
JOIN Customer c ON o.Customer_ID = c.Customer_ID
JOIN Staff s ON o.Delivery_Person = s.Staff_ID
LEFT JOIN Order_Pizza op ON o.Order_ID = op.Order_ID
LEFT JOIN Pizza p ON op.Pizza_ID = p.Pizza_ID
LEFT JOIN Order_Extras oe ON o.Order_ID = oe.Order_ID
LEFT JOIN Drink d ON oe.Drink_ID = d.Drink_ID
LEFT JOIN Dessert ds ON oe.Dessert_ID = ds.Dessert_ID
LEFT JOIN Discount dis ON o.Discount_Code = dis.Discount_Code
ORDER BY o.Order_ID;''')
rows = cursor.fetchall()

print("\n📋 Customers in database:")
for row in rows:
    print(f"- {row[0]} ({row[1]})")

# Close connection
conn.commit()
conn.close()
print("\n🎉 Setup complete!")
