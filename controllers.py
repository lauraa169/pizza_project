# README: this file contains all the business logic for the app
# such as how we define vegan and vegetarian pizzas, how we calculate prices, etc.
from sqlalchemy.orm import selectinload

from app import no_driver_available
from models import *
from datetime import datetime, date, timedelta
from sqlalchemy import func, extract, case, and_


def get_pizzas(session):
    pizzas = session.query(Pizza).order_by(Pizza.Pizza_ID).all()
    return pizzas

def get_items(session):
    items = session.query(MenuItem).order_by(MenuItem.Item_ID).all()
    return items

def get_valid_codes(session):
    valid_codes = {row[0] for row in session.query(Discount.Discount_Code).all()}
    return valid_codes

def populate_vegan(session):
    pizzas = get_pizzas(session)
    for p in pizzas:
        p.Vegan_Pizza = is_vegan_pizza(session, p.Pizza_ID)
    # session.commit()

def populate_vegetarian(session):
    pizzas = get_pizzas(session)
    for p in pizzas:
        p.Vegetarian_Pizza = is_vegetarian_pizza(session, p.Pizza_ID)
    # session.commit()

def is_vegan_pizza(session, pizza_id: int) -> bool:
    # joins Pizza_Ingredient -> Ingredient and check if any ingredient is non-vegan
    non_vegan_exists = (
        session.query(Ingredient)
        .join(PizzaIngredient, Ingredient.Ingredient_ID == PizzaIngredient.c.Ingredient_ID)
        .filter(
            PizzaIngredient.c.Pizza_ID == pizza_id,
            Ingredient.Vegan_Ingredient.is_(False)
        )
        .first()
        is not None
        # returns true if the pizza contains a non-vegan ingredient
    )
    # returns True if no non-vegan ingredients
    return not non_vegan_exists

def is_vegetarian_pizza(session, pizza_id: int) -> bool:
    # joins Pizza_Ingredient -> Ingredient and check if any ingredient is non-vegan
    non_vegetarian_exists = (
        session.query(Ingredient)
        .join(PizzaIngredient, Ingredient.Ingredient_ID == PizzaIngredient.c.Ingredient_ID)
        .filter(
            PizzaIngredient.c.Pizza_ID == pizza_id,
            Ingredient.Vegetarian_Ingredient.is_(False)
        )
        .first()
        is not None
        # returns true if the pizza contains a non-vegan ingredient
    )
    # returns True if no non-vegan ingredients
    return not non_vegetarian_exists

def calculate_price(session, pizza_id: int):
    # Get the pizza
    pizza = session.query(Pizza).filter(Pizza.Pizza_ID == pizza_id).one()

    # Sum the ingredient costs
    total_cost = float(sum(ing.Price for ing in pizza.ingredients) + 5)

    final_price = total_cost * 1.4 * 1.09

    return round(final_price, 2)

def new_order(session, customer_id: int,item_id: int, quantity: int, order_address: str, postal_code: str, order_price: int):
    with session.begin_nested():
        driver = assign_driver(session, postal_code)
        if driver is None:
            # keeps track of orders that dont go through for analytical purposes (report)
            undelivered_order(session, customer_id, order_address, postal_code, order_price)
            # calls no driver available interface
            no_driver_available(session)


        order = Order(Customer_ID=customer_id, Delivery_Person=driver, Order_Address=order_address,
                  Order_Postal_Code=postal_code, Order_Time=datetime.now(), Order_Price=order_price, Delivered=True)
        session.add(order)
        session.flush()

        increase_pizzas_ordered(session, customer_id)
        order_item(session, order.Order_ID, item_id, quantity)
        return order.Order_ID

def undelivered_order(session, customer_id: int, order_address: str, postal_code: str, order_price: int):
    with session.begin_nested():
        undeliveredOrder = Undelivered_Order(Customer_ID=customer_id, UOrder_Address=order_address, UOrder_Postal_Code=postal_code,UOrder_Time=datetime.now(), UOrder_Price=order_price )
        session.add(undeliveredOrder)
        session.flush()
        return undeliveredOrder.UOrder_ID

def assign_driver(session, postal_code: str):
    drivers = session.query(Staff).filter(Staff.Postal_Code == postal_code).all()
    for driver in drivers:
        if driver.Availability() is True:
            session.query(Staff).filter(Staff.Staff_ID == driver.Staff_ID).update({"Busy_Until": datetime.now() + timedelta(minutes=30)})
            return driver.Staff_ID
    return None

def order_item(session, order_id:int, item_id: int, quantity: int):
    with session.begin_nested():
        item_ordered = OrderItemLink(Order_ID=order_id, Item_ID=item_id, Quantity=quantity)
        session.add(item_ordered)
        # session.commit()

def increase_pizzas_ordered(session, customer_id: int):
    customer = session.query(Customer).filter(Customer.Customer_ID == customer_id).one()
    customer.Pizzas_Ordered += 1

def apply_discount(session, order_price: int, discount_code):
    with session.begin_nested():
        discount = session.query(Discount).filter(Discount.Discount_Code == discount_code).one()
        if discount.Redeemed is False:
            order_price -= (order_price * discount.Percent) / 100
            discount.Redeemed = True
        else:
            print("Sorry! this discount code has already been redeemed.")
        # session.commit()
        return order_price

def loyalty_discount(session, customer_id: int, order_price: int):
    customer = session.query(Customer).filter(Customer.Customer_ID == customer_id).one()
    if customer.Pizzas_Ordered > 0 and customer.Pizzas_Ordered % 10 == 0:
        print("You have received a loyalty discount!")
        return order_price * 0.9
    return order_price

def birthday_discount(session, customer_id: int, order_id: int, order_price: int):
    customer = session.query(Customer).filter(Customer.Customer_ID == customer_id).one()
    today = date.today()

    if customer.Birth_Date.day == today.day and customer.Birth_Date.month == today.month:
        items = session.query(OrderItemLink).filter(OrderItemLink.Order_ID == order_id).all()
        cheapest_pizza = 100
        cheapest_drink = 100

        for item in items:
            if 0 < item.Item_ID <= 10:
                cheapest_pizza = min(cheapest_pizza, calculate_price(session, item.Item_ID))
            elif 10 < item.Item_ID <= 20:
                price = session.query(MenuItem).filter(item.Item_ID == MenuItem.Item_ID).one()
                cheapest_drink = min(cheapest_drink, price[2])

        if cheapest_drink == 100: cheapest_drink = 0

        print("It's your Birthday! You received only the cheapest items for free as we need as much profit as possible.")
        return order_price - cheapest_drink - cheapest_pizza

    return order_price

def checkout(session, order_id: int, discount_code: int):
    with session.begin_nested():
        items = session.query(OrderItemLink).filter(OrderItemLink.Order_ID == order_id).all()
        order = session.query(Order).filter(Order.Order_ID == order_id).one()
        price = 0
        for item in items:
            if 0 < item.Item_ID <= 10:
                price += (calculate_price(session,item.Item_ID) * item.Quantity)
            else:
                price += (item.Item_Price * item.Quantity)
        if discount_code is not None:
            order.Discount_Code = discount_code
            total_price = apply_discount(session, price, discount_code)
        else:
            total_price = price

        total_price = birthday_discount(session, order.Customer_ID, order_id,
                                        (loyalty_discount(session, order.Customer_ID, total_price)))

        print(f"Total price: {round(total_price, 2)}" +
              "\nThank you for your order!" +
              "\nWe hope to see you again soon!")

def top3pizzas (session):
    top_pizzas = session.query(
        Pizza.Pizza_Name,
        func.sum(OrderItemLink.Quantity).label('total_sold')
    ).join(OrderItemLink, Pizza.Pizza_ID == OrderItemLink.Item_ID) \
        .group_by(Pizza.Pizza_Name) \
        .order_by(func.sum(OrderItemLink.Quantity).desc()) \
        .limit(3) \
        .all()

    print("Top 3 Selling Pizzas:")
    for pizza_name, quantity in top_pizzas:
        print(f"- {pizza_name}: {quantity} units sold")

def check_undelivered_orders(session):
    undelivered = session.query(Undelivered_Order).all()
    if not undelivered:
        print("No undelivered orders!")
    else:
        for item in undelivered:
            print(item)

def monthly_earnings_gender(session, year: int, month: int):
    monthly_earnings = session.query(
        Staff.Gender,
        func.sum(Order.Order_Price).label('total_monthly_earnings')
    ).join(Order, Staff.Staff_ID == Order.Delivery_Person) \
    .filter(func.strftime("%Y", Order.Order_Time) == str(year)) \
    .filter(func.strftime("%m", Order.Order_Time) == f"{month:02d}") \
    .group_by(Staff.Gender) \
    .order_by(func.sum(Order.Order_Price).desc()) \
    .all()

    return monthly_earnings

def monthly_earnings_postal(session, postal_code):
    results = (
        session.query(
            Staff.Staff_ID,
            Staff.Name,
            Staff.Surname,
            extract('year', Order.Order_Time).label('year'),
            extract('month', Order.Order_Time).label('month'),
            func.sum(Order.Order_Price).label('total_earnings')
        )
        .join(Order, Order.Delivery_Person == Staff.Staff_ID)
        .filter(
            Staff.Postal_Code == postal_code,
            Order.Delivered.is_(True)
        )
        .group_by(Staff.Staff_ID, Staff.Name, Staff.Surname, 'year', 'month')
        .order_by(Staff.Staff_ID, 'year', 'month')
        .all()
    )

    if not results:
        print(f"No delivered orders found for postal code {postal_code}.")
        return []

    print(f"\nMonthly earnings by staff for postal code {postal_code}:")
    for sid, name, surname, year, month, earnings in results:
        print(f"  {name} {surname} (ID: {sid}) - {int(year)}-{int(month):02d}: ${float(earnings):.2f}")

    return results

def monthly_earnings_age(session, year: int, month: int):
    age_group_case = case(
        (and_(Staff.Age >= 16, Staff.Age <= 21), "16 to 21"),
        (and_(Staff.Age >= 22, Staff.Age <= 40), "22 to 40"),
        (Staff.Age > 40, "40+"),
        else_="Unknown"  # Fallback for ages outside defined ranges (e.g., <16)
    ).label("age_group")  # Assign a label to the computed column

    earnings_by_age_group = session.query(
        age_group_case,  # Select the computed age group label
        func.sum(Order.Order_Price).label('total_monthly_earnings')
    ).join(Order, Staff.Staff_ID == Order.Delivery_Person) \
        .filter(func.strftime("%Y", Order.Order_Time) == str(year)) \
        .filter(func.strftime("%m", Order.Order_Time) == f"{month:02d}") \
        .group_by(age_group_case) \
        .order_by(age_group_case) \
        .all()

    return earnings_by_age_group
