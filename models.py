# README:
# Declarative SQLAlchemy 2.x models with a plain Declarative Base (no Flask-SQLAlchemy)

from datetime import datetime, date
from typing import List

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Column,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


class Base(DeclarativeBase):
    pass


# Association table for many-to-many between Pizza and Ingredient
PizzaIngredient = Table(
    "Pizza_Ingredient",
    Base.metadata,
    Column("Pizza_ID", Integer, ForeignKey("Pizza.Pizza_ID"), primary_key=True),
    Column("Ingredient_ID", Integer, ForeignKey("Ingredient.Ingredient_ID"), primary_key=True),
)


class Discount(Base):
    __tablename__ = "Discount"
    Discount_Code: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    Percent: Mapped[int] = mapped_column(Integer, nullable=False)
    Redeemed: Mapped[bool] = mapped_column(Boolean, nullable=False)

    __table_args__ = (
        CheckConstraint("Percent >= 0 AND Percent <= 100", name="ck_discount_percent_range"),
    )


class Customer(Base):
    __tablename__ = "Customer"
    Customer_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Customer_Name: Mapped[str] = mapped_column(String, nullable=False)
    Customer_Surname: Mapped[str] = mapped_column(String, nullable=False)
    Birth_Date: Mapped[date] = mapped_column(Date, nullable=False)
    Customer_Address: Mapped[str] = mapped_column(String, nullable=False)
    Customer_Postal_Code: Mapped[str] = mapped_column(String, nullable=False)
    Credit_Card: Mapped[int] = mapped_column(BigInteger, nullable=False)
    Customer_Email: Mapped[str] = mapped_column(String, nullable=False)
    Phone_Number: Mapped[int] = mapped_column(BigInteger, nullable=False)
    Pizzas_Ordered: Mapped[int] = mapped_column(Integer, nullable=False)

    orders: Mapped[List["Order"]] = relationship(back_populates="customer")


class Staff(Base):
    __tablename__ = "Staff"
    Staff_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(String, nullable=False)
    Surname: Mapped[str] = mapped_column(String, nullable=False)
    Bank_Account: Mapped[str] = mapped_column(String, nullable=False)
    Liscence: Mapped[int] = mapped_column(Integer, nullable=False)
    Postal_Code: Mapped[str] = mapped_column(String, nullable=False)
    Availability: Mapped[bool] = mapped_column(Boolean, nullable=False)

    deliveries: Mapped[List["Order"]] = relationship(back_populates="delivery_person")


class MenuItem(Base):
    __tablename__ = "Menu_Item"
    Item_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Item_Name: Mapped[str] = mapped_column(String, nullable=False)
    Item_Price: Mapped[Numeric] = mapped_column(Numeric(5, 2), nullable=True)


class Drink(Base):
    __tablename__ = "Drink"
    Drink_ID: Mapped[int] = mapped_column(ForeignKey("Menu_Item.Item_ID"), primary_key=True)
    Drink_Name: Mapped[str] = mapped_column(String, nullable=False)
    Drink_Price: Mapped[Numeric] = mapped_column(Numeric(5, 2), nullable=False)
    is_18_plus: Mapped[bool] = mapped_column("18+", Boolean, nullable=False)


class Dessert(Base):
    __tablename__ = "Dessert"
    Dessert_ID: Mapped[int] = mapped_column(ForeignKey("Menu_Item.Item_ID"), primary_key=True)
    Dessert_Name: Mapped[str] = mapped_column(String, nullable=False)
    Dessert_Price: Mapped[Numeric] = mapped_column(Numeric(5, 2), nullable=False)


class Ingredient(Base):
    __tablename__ = "Ingredient"
    Ingredient_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Ingredient_Name: Mapped[str] = mapped_column(String, nullable=False)
    Price: Mapped[Numeric] = mapped_column(Numeric(5, 2), nullable=False)
    Vegetarian_Ingredient: Mapped[bool] = mapped_column(Boolean, nullable=False)
    Vegan_Ingredient: Mapped[bool] = mapped_column(Boolean, nullable=False)

    pizzas: Mapped[List["Pizza"]] = relationship(
        secondary=PizzaIngredient,
        back_populates="ingredients",
        lazy="selectin",
    )


class Pizza(Base):
    __tablename__ = "Pizza"
    Pizza_ID: Mapped[int] = mapped_column(ForeignKey("Menu_Item.Item_ID"), primary_key=True)
    Pizza_Name: Mapped[str] = mapped_column(String, nullable=False)
    Vegetarian_Pizza: Mapped[bool | None] = mapped_column(Boolean)
    Vegan_Pizza: Mapped[bool | None] = mapped_column(Boolean)

    ingredients: Mapped[List[Ingredient]] = relationship(
        secondary=PizzaIngredient,
        back_populates="pizzas",
        lazy="selectin",
    )


class Order(Base):
    __tablename__ = "Order"
    Order_ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Customer_ID: Mapped[int] = mapped_column(ForeignKey("Customer.Customer_ID"), nullable=False)
    Delivery_Person: Mapped[int] = mapped_column(ForeignKey("Staff.Staff_ID"), nullable=False)
    Discount_Code: Mapped[int | None] = mapped_column(ForeignKey("Discount.Discount_Code"))
    Order_Address: Mapped[str] = mapped_column(String, nullable=False)
    Order_Postal_Code: Mapped[str] = mapped_column(String, nullable=False)
    Order_Time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    Order_Price: Mapped[int] = mapped_column(BigInteger, nullable=False)
    Delivered: Mapped[bool] = mapped_column(Boolean, nullable=False)

    customer: Mapped[Customer] = relationship(back_populates="orders")
    delivery_person: Mapped[Staff] = relationship(back_populates="deliveries")
    items: Mapped[List["OrderItemLink"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderItemLink(Base):
    __tablename__ = "Order_Item"
    Order_ID: Mapped[int] = mapped_column(ForeignKey("Order.Order_ID"), primary_key=True)
    Item_ID: Mapped[int] = mapped_column(ForeignKey("Menu_Item.Item_ID"), primary_key=True)
    Quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped[Order] = relationship(back_populates="items")
    menu_item: Mapped[MenuItem] = relationship()


# Seed function rewritten to use a provided Session
def seed_data(session: Session) -> None:
    if session.query(Discount).count() == 0:
        session.add_all([
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

    if session.query(Customer).count() == 0:
        session.add_all([
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

    if session.query(MenuItem).count() == 0:
        menu_items = [
            # Pizzas (IDs 1..10)
            ("Margherita", None), ("Pepperoni", None), ("Hawaiian", None), ("BBQ Chicken", None),
            ("Veggie Supreme", None), ("Four Cheese", None), ("Meat Feast", None), ("Spicy Veggie", None),
            ("Seafood Special", None), ("Mushroom Delight", None),
            # Drinks (IDs 11..20)
            ("Cola", 2.50), ("Orange Juice", 3.00), ("Lemonade", 2.20), ("Iced Tea", 2.80),
            ("Beer", 4.00), ("Red Wine", 5.50), ("Water", 1.50), ("Energy Drink", 3.50),
            ("Apple Juice", 3.00), ("Whiskey", 6.50),
            # Desserts (IDs 21..30)
            ("Ice Cream", 3.50), ("Cheesecake", 4.00), ("Brownie", 3.00), ("Tiramisu", 4.50),
            ("Apple Pie", 3.80), ("Chocolate Cake", 4.20), ("Panna Cotta", 3.90), ("Donut", 2.50),
            ("Fruit Salad", 3.20), ("Cupcake", 2.80),
        ]
        session.add_all([MenuItem(Item_Name=n, Item_Price=p) for n, p in menu_items])
        session.flush()

        drinks = [
            (11, "Cola", 2.50, False), (12, "Orange Juice", 3.00, False), (13, "Lemonade", 2.20, False),
            (14, "Iced Tea", 2.80, False), (15, "Beer", 4.00, True), (16, "Red Wine", 5.50, True),
            (17, "Water", 1.50, False), (18, "Energy Drink", 3.50, False), (19, "Apple Juice", 3.00, False),
            (20, "Whiskey", 6.50, True),
        ]
        session.add_all([
            Drink(Drink_ID=i, Drink_Name=n, Drink_Price=p, is_18_plus=is18)
            for (i, n, p, is18) in drinks
        ])

        desserts = [
            (21, "Ice Cream", 3.50), (22, "Cheesecake", 4.00), (23, "Brownie", 3.00), (24, "Tiramisu", 4.50),
            (25, "Apple Pie", 3.80), (26, "Chocolate Cake", 4.20), (27, "Panna Cotta", 3.90), (28, "Donut", 2.50),
            (29, "Fruit Salad", 3.20), (30, "Cupcake", 2.80),
        ]
        session.add_all([Dessert(Dessert_ID=i, Dessert_Name=n, Dessert_Price=p) for (i, n, p) in desserts])

        pizzas = [
            (1, "Margherita", None, None),
            (2, "Pepperoni", None, None),
            (3, "Hawaiian", None, None),
            (4, "BBQ Chicken", None, None),
            (5, "Veggie Supreme", None, None),
            (6, "Four Cheese", None, None),
            (7, "Meat Feast", None, None),
            (8, "Spicy Veggie", None, None),
            (9, "Seafood Special", None, None),
            (10, "Mushroom Delight", None, None),
        ]
        session.add_all([
            Pizza(Pizza_ID=i, Pizza_Name=n, Vegetarian_Pizza=veg, Vegan_Pizza=vegan)
            for (i, n, veg, vegan) in pizzas
        ])

    if session.query(Ingredient).count() == 0:
        session.add_all([
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
        session.flush()

        ing_ids = {ing.Ingredient_Name: ing.Ingredient_ID for ing in session.query(Ingredient).all()}

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
        session.execute(PizzaIngredient.insert(), [{"Pizza_ID": p, "Ingredient_ID": i} for p, i in links])

    if session.query(Order).count() == 0:
        session.add_all([
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

    if session.query(OrderItemLink).count() == 0:
        session.add_all([
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

    session.commit()