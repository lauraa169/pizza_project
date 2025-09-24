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
    print("✅ Basic data inserted successfully.")

    # Step 4: Label vegan pizzas:
    cursor.execute("SELECT Pizza_ID FROM Pizza")
    pizzas = cursor.fetchall()
    for pizza in pizzas:
        pizzaID = pizza[0]
        vegan = 1 if is_vegan(conn,pizzaID) else 0
        cursor.execute("UPDATE pizza SET Vegan_Pizza = ? WHERE Pizza_ID = ?", (vegan, pizza[0]))
    conn.commit()
    print("✅ Vegan pizzas labeled successfully.")

def test_query():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Example: list all vegan pizzas
    print("✅ Vegan Pizzas:")
    cursor.execute("SELECT * FROM Pizza WHERE Vegan_Pizza = 1;")
    rows = cursor.fetchall()  # fetch all results
    for row in rows:
        print(row)  # prints each row as a tuple

    cursor.execute("SELECT * FROM Pizza_Ingredient WHERE Pizza_ID = 8 ")
    rows = cursor.fetchall()
    print("✅ Pizzas in the database:")
    for row in rows:
        print(row)  # prints each row as a tuple

    # Example: list all customers
    cursor.execute("SELECT * FROM Customer;")
    customers = cursor.fetchall()
    print("\n✅ Customers in the database:")
    for customer in customers:
        print(customer)

    print(is_vegan(conn,8))

    conn.close()

def display_menu():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Menu_Item;")
    items = cursor.fetchall()
    print("Menu Items:")
    print("----------")
    print("ID | Name | Price")
    print("----------")
    print("Pizzas:")
    for i in range(10):
        print(str(items[i][0]) + " | " + str(items[i][1]) + " .......... " + str(items[i][2]))
    print("----------")
    print("Drinks:")
    for i in range(10, 20):
        print(str(items[i][0]) + " | " + str(items[i][1]) + " .......... " + str(items[i][2]))
    print("----------")
    print("Desserts:")
    for i in range(20, 30):
        print(str(items[i][0]) + " | " + str(items[i][1]) + " .......... " + str(items[i][2]))

    conn.close()
def is_vegan(conn,pizza_id):
    cursor = conn.cursor()
    cursor.execute("SELECT Ingredient_ID FROM Pizza_Ingredient WHERE Pizza_ID = ?"
                   , (pizza_id,))
    ingredients = cursor.fetchall()
    vegan = True
    for ingredient in ingredients:
        cursor.execute("SELECT Vegan_Ingredient FROM Ingredient WHERE Ingredient.Ingredient_ID = ?"
                       , (ingredient[0],))
        if cursor.fetchone()[0] == 0:
            vegan = False
    return vegan





setup()
test_query()

