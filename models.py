# README: 
# Single CamelCase schema only. Removes Product/products and modern ecommerce layer.
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

from application import is_vegan

db = SQLAlchemy()

# Association table for many-to-many between Pizza and Ingredient
PizzaIngredient = db.Table(
    "Pizza_Ingredient",
    db.Column("Pizza_ID", db.Integer, db.ForeignKey("Pizza.Pizza_ID"), primary_key=True),
    db.Column("Ingredient_ID", db.Integer, db.ForeignKey("Ingredient.Ingredient_ID"), primary_key=True),
)

class Discount(db.Model):
    __tablename__ = "Discount"
    Discount_Code = db.Column(db.BigInteger, primary_key=True)
    Percent = db.Column(db.Integer, nullable=False)
    Redeemed = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        CheckConstraint("Percent >= 0 AND Percent <= 100", name="ck_discount_percent_range"),
    )

class Customer(db.Model):
    __tablename__ = "Customer"
    Customer_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_Name = db.Column(db.String, nullable=False)
    Customer_Surname = db.Column(db.String, nullable=False)
    Birth_Date = db.Column(db.Date, nullable=False)
    Customer_Address = db.Column(db.String, nullable=False)
    Customer_Postal_Code = db.Column(db.String, nullable=False)
    Credit_Card = db.Column(db.BigInteger, nullable=False)
    Customer_Email = db.Column(db.String, nullable=False)
    Phone_Number = db.Column(db.BigInteger, nullable=False)
    Pizzas_Ordered = db.Column(db.Integer, nullable=False)

    orders = db.relationship("Order", back_populates="customer")

class Staff(db.Model):
    __tablename__ = "Staff"
    Staff_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    Surname = db.Column(db.String, nullable=False)
    Bank_Account = db.Column(db.String, nullable=False)
    Liscence = db.Column(db.Integer, nullable=False)
    Postal_Code = db.Column(db.String, nullable=False)
    Availability = db.Column(db.Boolean, nullable=False)

    deliveries = db.relationship("Order", back_populates="delivery_person")

class MenuItem(db.Model):
    __tablename__ = "Menu_Item"
    Item_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Item_Name = db.Column(db.String, nullable=False)
    Item_Price = db.Column(db.Numeric(5, 2), nullable=False)

class Drink(db.Model):
    __tablename__ = "Drink"
    Drink_ID = db.Column(db.Integer, db.ForeignKey("Menu_Item.Item_ID"), primary_key=True)
    Drink_Name = db.Column(db.String, nullable=False)
    Drink_Price = db.Column(db.Numeric(5, 2), nullable=False)
    is_18_plus = db.Column("18+", db.Boolean, nullable=False)

class Dessert(db.Model):
    __tablename__ = "Dessert"
    Dessert_ID = db.Column(db.Integer, db.ForeignKey("Menu_Item.Item_ID"), primary_key=True)
    Dessert_Name = db.Column(db.String, nullable=False)
    Dessert_Price = db.Column(db.Numeric(5, 2), nullable=False)

class Ingredient(db.Model):
    __tablename__ = "Ingredient"
    Ingredient_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Ingredient_Name = db.Column(db.String, nullable=False)
    Price = db.Column(db.Numeric(5, 2), nullable=False)
    Vegetarian_Ingredient = db.Column(db.Boolean, nullable=False)
    Vegan_Ingredient = db.Column(db.Boolean, nullable=False)

class Pizza(db.Model):
    __tablename__ = "Pizza"
    Pizza_ID = db.Column(db.Integer, db.ForeignKey("Menu_Item.Item_ID"), primary_key=True)
    Pizza_Name = db.Column(db.String, nullable=False)
    Vegetarian_Pizza = db.Column(db.Boolean)
    Vegan_Pizza = db.Column(db.Boolean)
    Size = db.Column(db.Boolean, nullable=False)
    Pizza_Price = db.Column(db.Numeric(5, 2), nullable=False)

    ingredients = db.relationship(
        "Ingredient",
        secondary=PizzaIngredient,
        backref=db.backref("pizzas", lazy="dynamic"),
        lazy="joined",
    )

class Order(db.Model):
    __tablename__ = "Order"
    Order_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_ID = db.Column(db.Integer, db.ForeignKey("Customer.Customer_ID"), nullable=False)
    Delivery_Person = db.Column(db.Integer, db.ForeignKey("Staff.Staff_ID"), nullable=False)
    Discount_Code = db.Column(db.BigInteger, db.ForeignKey("Discount.Discount_Code"))
    Order_Address = db.Column(db.String, nullable=False)
    Order_Postal_Code = db.Column(db.String, nullable=False)
    Order_Time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Order_Price = db.Column(db.BigInteger, nullable=False)
    Delivered = db.Column(db.Boolean, nullable=False)

    customer = db.relationship("Customer", back_populates="orders")
    delivery_person = db.relationship("Staff", back_populates="deliveries")
    items = db.relationship("OrderItemLink", back_populates="order", cascade="all, delete-orphan")

class OrderItemLink(db.Model):
    __tablename__ = "Order_Item"
    Order_ID = db.Column(db.Integer, db.ForeignKey("Order.Order_ID"), primary_key=True)
    Item_ID = db.Column(db.Integer, db.ForeignKey("Menu_Item.Item_ID"), primary_key=True)
    Quantity = db.Column(db.Integer, nullable=False)

    order = db.relationship("Order", back_populates="items")
    menu_item = db.relationship("MenuItem")

# Seed function remains, using CamelCase tables only
def seed_data():
    if Discount.query.count() == 0:
        db.session.add_all([
            Discount(Discount_Code=1001, Percent=10, Redeemed=False),
            Discount(Discount_Code=1002, Percent=15, Redeemed=True),
            Discount(Discount_Code=1003, Percent=20, Redeemed=False),
            Discount(Discount_Code=1004, Percent=5, Redeemed=True),
            Discount(Discount_Code=1005, Percent=25, Redeemed=False),
            Discount(Discount_Code=1006, Percent=30, Redeemed=True),
            Discount(Discount_Code=1007, Percent=12, Redeemed=False),
            Discount(Discount_Code=1008, Percent=18, Redeemed=False),
            Discount(Discount_Code=1009, Percent=8, Redeemed=True),
            Discount(Discount_Code=1010, Percent=22, Redeemed=False),
        ])

    if Customer.query.count() == 0:
        db.session.add_all([
            Customer(Customer_Name='John',  Customer_Surname='Doe',      Birth_Date=date(1990,5,15), Customer_Address='123 Main St',  Customer_Postal_Code='10001', Credit_Card=1234567890123456, Customer_Email='john@example.com',  Phone_Number=1112223333, Pizzas_Ordered=5),
            Customer(Customer_Name='Jane',  Customer_Surname='Smith',    Birth_Date=date(1985,8,22), Customer_Address='456 Park Ave', Customer_Postal_Code='10002', Credit_Card=9876543210987654, Customer_Email='jane@example.com',  Phone_Number=2223334444, Pizzas_Ordered=3),
            Customer(Customer_Name='Alice', Customer_Surname='Brown',    Birth_Date=date(2000,1,10), Customer_Address='789 Broadway', Customer_Postal_Code='10003', Credit_Card=1111222233334444, Customer_Email='alice@example.com', Phone_Number=3334445555, Pizzas_Ordered=7),
            Customer(Customer_Name='Bob',   Customer_Surname='Johnson',  Birth_Date=date(1992,3,18), Customer_Address='12 River Rd',  Customer_Postal_Code='10001', Credit_Card=5555444433332222, Customer_Email='bob@example.com',   Phone_Number=4445556666, Pizzas_Ordered=2),
            Customer(Customer_Name='Emily', Customer_Surname='Davis',    Birth_Date=date(1995,11,25),Customer_Address='45 Hill St',   Customer_Postal_Code='10002', Credit_Card=4444333322221111, Customer_Email='emily@example.com', Phone_Number=5556667777, Pizzas_Ordered=4),
            Customer(Customer_Name='Chris', Customer_Surname='Wilson',   Birth_Date=date(1988,7,30), Customer_Address='78 Lake Ave',  Customer_Postal_Code='10003', Credit_Card=6666777788889999, Customer_Email='chris@example.com', Phone_Number=6667778888, Pizzas_Ordered=6),
            Customer(Customer_Name='Sophia',Customer_Surname='Martinez', Birth_Date=date(1999,2,14), Customer_Address='90 Oak Ln',    Customer_Postal_Code='10001', Credit_Card=7777888899990000, Customer_Email='sophia@example.com',Phone_Number=7778889999, Pizzas_Ordered=8),
            Customer(Customer_Name='Liam',  Customer_Surname='Anderson', Birth_Date=date(1993,9,12), Customer_Address='22 Pine St',   Customer_Postal_Code='10002', Credit_Card=8888999900001111, Customer_Email='liam@example.com',  Phone_Number=8889990000, Pizzas_Ordered=1),
            Customer(Customer_Name='Olivia',Customer_Surname='Taylor',   Birth_Date=date(1997,12,1), Customer_Address='34 Maple Dr',  Customer_Postal_Code='10003', Credit_Card=9999000011112222, Customer_Email='olivia@example.com',Phone_Number=9990001111, Pizzas_Ordered=3),
            Customer(Customer_Name='Ethan', Customer_Surname='Harris',   Birth_Date=date(1989,4,9),  Customer_Address='56 Birch Blvd',Customer_Postal_Code='10001', Credit_Card=2222111133334444, Customer_Email='ethan@example.com', Phone_Number=1011121314, Pizzas_Ordered=9),
        ])

    if Staff.query.count() == 0:
        db.session.add_all([
            Staff(Name='Mark',  Surname='Taylor',  Bank_Account='BA12345', Liscence=1,  Postal_Code='10001', Availability=True),
            Staff(Name='Lucy',  Surname='Green',   Bank_Account='BA67890', Liscence=2,  Postal_Code='10002', Availability=True),
            Staff(Name='Paul',  Surname='White',   Bank_Account='BA54321', Liscence=3,  Postal_Code='10003', Availability=True),
            Staff(Name='Anna',  Surname='King',    Bank_Account='BA98765', Liscence=4,  Postal_Code='10001', Availability=True),
            Staff(Name='Tom',   Surname='Evans',   Bank_Account='BA19283', Liscence=5,  Postal_Code='10002', Availability=False),
            Staff(Name='Rachel',Surname='Scott',   Bank_Account='BA45678', Liscence=6,  Postal_Code='10003', Availability=True),
            Staff(Name='James', Surname='Lee',     Bank_Account='BA22222', Liscence=7,  Postal_Code='10001', Availability=True),
            Staff(Name='Maria', Surname='Hall',    Bank_Account='BA33333', Liscence=8,  Postal_Code='10002', Availability=True),
            Staff(Name='David', Surname='Young',   Bank_Account='BA44444', Liscence=9,  Postal_Code='10003', Availability=True),
            Staff(Name='Sophia',Surname='Clark',   Bank_Account='BA55555', Liscence=10, Postal_Code='10001', Availability=True),
        ])

    if MenuItem.query.count() == 0:
        menu_items = [
            # Pizzas (IDs 1..10)
            ("Margherita", 8.50), ("Pepperoni", 9.50), ("Hawaiian", 10.00), ("BBQ Chicken", 11.00),
            ("Veggie Supreme", 9.00), ("Four Cheese", 10.50), ("Meat Feast", 12.00), ("Spicy Veggie", 9.50),
            ("Seafood Special", 13.00), ("Mushroom Delight", 9.00),
            # Drinks (IDs 11..20)
            ("Cola", 2.50), ("Orange Juice", 3.00), ("Lemonade", 2.20), ("Iced Tea", 2.80),
            ("Beer", 4.00), ("Red Wine", 5.50), ("Water", 1.50), ("Energy Drink", 3.50),
            ("Apple Juice", 3.00), ("Whiskey", 6.50),
            # Desserts (IDs 21..30)
            ("Ice Cream", 3.50), ("Cheesecake", 4.00), ("Brownie", 3.00), ("Tiramisu", 4.50),
            ("Apple Pie", 3.80), ("Chocolate Cake", 4.20), ("Panna Cotta", 3.90), ("Donut", 2.50),
            ("Fruit Salad", 3.20), ("Cupcake", 2.80),
        ]
        db.session.add_all([MenuItem(Item_Name=n, Item_Price=p) for n, p in menu_items])
        db.session.flush()

        drinks = [
            (11, "Cola", 2.50, False), (12, "Orange Juice", 3.00, False), (13, "Lemonade", 2.20, False),
            (14, "Iced Tea", 2.80, False), (15, "Beer", 4.00, True), (16, "Red Wine", 5.50, True),
            (17, "Water", 1.50, False), (18, "Energy Drink", 3.50, False), (19, "Apple Juice", 3.00, False),
            (20, "Whiskey", 6.50, True),
        ]
        db.session.add_all([
            Drink(Drink_ID=i, Drink_Name=n, Drink_Price=p, is_18_plus=is18)
            for (i, n, p, is18) in drinks
        ])

        desserts = [
            (21, "Ice Cream", 3.50), (22, "Cheesecake", 4.00), (23, "Brownie", 3.00), (24, "Tiramisu", 4.50),
            (25, "Apple Pie", 3.80), (26, "Chocolate Cake", 4.20), (27, "Panna Cotta", 3.90), (28, "Donut", 2.50),
            (29, "Fruit Salad", 3.20), (30, "Cupcake", 2.80),
        ]
        db.session.add_all([Dessert(Dessert_ID=i, Dessert_Name=n, Dessert_Price=p) for (i, n, p) in desserts])

        pizzas = [
            (1, "Margherita", None, is_vegan(1), True, 8.50),
            (2, "Pepperoni", None, is_vegan(2), True, 9.50),
            (3, "Hawaiian", None, is_vegan(3), True, 10.00),
            (4, "BBQ Chicken", None, is_vegan(4), True, 11.00),
            (5, "Veggie Supreme", None, is_vegan(5), True, 9.00),
            (6, "Four Cheese", None, is_vegan(6), True, 10.50),
            (7, "Meat Feast", None, is_vegan(7), True, 12.00),
            (8, "Spicy Veggie", None, is_vegan(8), True, 9.50),
            (9, "Seafood Special", None, is_vegan(9), True, 13.00),
            (10, "Mushroom Delight", None, is_vegan(10), True, 9.00),
        ]
        db.session.add_all([
            Pizza(Pizza_ID=i, Pizza_Name=n, Vegetarian_Pizza=veg, Vegan_Pizza=vegan, Size=size, Pizza_Price=price)
            for (i, n, veg, vegan, size, price) in pizzas
        ])

    if Ingredient.query.count() == 0:
        db.session.add_all([
            Ingredient(Ingredient_Name='Cheese',         Price=1.00, Vegetarian_Ingredient=True,  Vegan_Ingredient=False),
            Ingredient(Ingredient_Name='Tomato Sauce',   Price=0.50, Vegetarian_Ingredient=True,  Vegan_Ingredient=True),
            Ingredient(Ingredient_Name='Pepperoni',      Price=1.50, Vegetarian_Ingredient=False, Vegan_Ingredient=False),
            Ingredient(Ingredient_Name='Ham',            Price=1.50, Vegetarian_Ingredient=False, Vegan_Ingredient=False),
            Ingredient(Ingredient_Name='Chicken',        Price=1.80, Vegetarian_Ingredient=False, Vegan_Ingredient=False),
            Ingredient(Ingredient_Name='Mushrooms',      Price=1.20, Vegetarian_Ingredient=True,  Vegan_Ingredient=True),
            Ingredient(Ingredient_Name='Onions',         Price=0.80, Vegetarian_Ingredient=True,  Vegan_Ingredient=True),
            Ingredient(Ingredient_Name='Bell Peppers',   Price=0.90, Vegetarian_Ingredient=True,  Vegan_Ingredient=True),
            Ingredient(Ingredient_Name='Olives',         Price=1.00, Vegetarian_Ingredient=True,  Vegan_Ingredient=True),
            Ingredient(Ingredient_Name='Shrimp',         Price=2.50, Vegetarian_Ingredient=False, Vegan_Ingredient=False),
        ])
        db.session.flush()

        ing_ids = {ing.Ingredient_Name: ing.Ingredient_ID for ing in Ingredient.query.all()}

        links = [
            (1, ing_ids['Cheese']), (1, ing_ids['Tomato Sauce']),
            (2, ing_ids['Cheese']), (2, ing_ids['Tomato Sauce']), (2, ing_ids['Pepperoni']),
            (3, ing_ids['Cheese']), (3, ing_ids['Tomato Sauce']), (3, ing_ids['Ham']),
            (4, ing_ids['Cheese']), (4, ing_ids['Tomato Sauce']), (4, ing_ids['Chicken']),
            (5, ing_ids['Cheese']), (5, ing_ids['Tomato Sauce']), (5, ing_ids['Mushrooms']),
            (5, ing_ids['Onions']), (5, ing_ids['Bell Peppers']), (5, ing_ids['Olives']),
            (6, ing_ids['Cheese']), (6, ing_ids['Tomato Sauce']),
            (7, ing_ids['Cheese']), (7, ing_ids['Tomato Sauce']), (7, ing_ids['Pepperoni']),
            (7, ing_ids['Ham']), (7, ing_ids['Chicken']),
            (8, ing_ids['Tomato Sauce']), (8, ing_ids['Mushrooms']), (8, ing_ids['Onions']),
            (8, ing_ids['Bell Peppers']), (8, ing_ids['Olives']),
            (9, ing_ids['Cheese']), (9, ing_ids['Tomato Sauce']), (9, ing_ids['Shrimp']),
            (10, ing_ids['Cheese']), (10, ing_ids['Tomato Sauce']), (10, ing_ids['Mushrooms']),
        ]
        db.session.execute(PizzaIngredient.insert(), [{"Pizza_ID": p, "Ingredient_ID": i} for p, i in links])

    if Order.query.count() == 0:
        db.session.add_all([
            Order(Customer_ID=1,  Delivery_Person=1,  Discount_Code=1001, Order_Address='123 Main St', Order_Postal_Code='10001', Order_Time=datetime(2025,1,1,18,0,0),  Order_Price=25, Delivered=True),
            Order(Customer_ID=2,  Delivery_Person=2,  Discount_Code=1002, Order_Address='456 Park Ave',Order_Postal_Code='10002', Order_Time=datetime(2025,1,2,19,30,0), Order_Price=40, Delivered=False),
            Order(Customer_ID=3,  Delivery_Person=3,  Discount_Code=None, Order_Address='789 Broadway',Order_Postal_Code='10003', Order_Time=datetime(2025,1,3,20,0,0),  Order_Price=30, Delivered=True),
            Order(Customer_ID=4,  Delivery_Person=4,  Discount_Code=1004, Order_Address='12 River Rd', Order_Postal_Code='10001', Order_Time=datetime(2025,1,4,18,45,0), Order_Price=22, Delivered=True),
            Order(Customer_ID=5,  Delivery_Person=5,  Discount_Code=1005, Order_Address='45 Hill St',  Order_Postal_Code='10002', Order_Time=datetime(2025,1,5,21,15,0), Order_Price=28, Delivered=False),
            Order(Customer_ID=6,  Delivery_Person=6,  Discount_Code=None, Order_Address='78 Lake Ave', Order_Postal_Code='10003', Order_Time=datetime(2025,1,6,17,30,0), Order_Price=35, Delivered=True),
            Order(Customer_ID=7,  Delivery_Person=7,  Discount_Code=1007, Order_Address='90 Oak Ln',   Order_Postal_Code='10001', Order_Time=datetime(2025,1,7,20,20,0), Order_Price=42, Delivered=True),
            Order(Customer_ID=8,  Delivery_Person=8,  Discount_Code=1008, Order_Address='22 Pine St',  Order_Postal_Code='10002', Order_Time=datetime(2025,1,8,19,10,0), Order_Price=18, Delivered=False),
            Order(Customer_ID=9,  Delivery_Person=9,  Discount_Code=1009, Order_Address='34 Maple Dr', Order_Postal_Code='10003', Order_Time=datetime(2025,1,9,18,40,0), Order_Price=50, Delivered=True),
            Order(Customer_ID=10, Delivery_Person=10, Discount_Code=1010, Order_Address='56 Birch Blvd',Order_Postal_Code='10001',Order_Time=datetime(2025,1,10,21,0,0), Order_Price=60, Delivered=True),
        ])

    if OrderItemLink.query.count() == 0:
        db.session.add_all([
            OrderItemLink(Order_ID=1,  Item_ID=1,  Quantity=2),
            OrderItemLink(Order_ID=1,  Item_ID=11, Quantity=1),
            OrderItemLink(Order_ID=2,  Item_ID=3,  Quantity=1),
            OrderItemLink(Order_ID=2,  Item_ID=15, Quantity=2),
            OrderItemLink(Order_ID=3,  Item_ID=5,  Quantity=1),
            OrderItemLink(Order_ID=4,  Item_ID=6,  Quantity=2),
            OrderItemLink(Order_ID=5,  Item_ID=7,  Quantity=1),
            OrderItemLink(Order_ID=6,  Item_ID=8,  Quantity=2),
            OrderItemLink(Order_ID=7,  Item_ID=9,  Quantity=1),
            OrderItemLink(Order_ID=10, Item_ID=10, Quantity=3),
        ])

    db.session.commit()
