# README: this file contains all the business logic for the app
# such as how we define vegan and vegetarian pizzas, how we calculate prices, etc.
from sqlalchemy.orm import selectinload
from models import *

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
    order = Order(Customer_ID=customer_id, Delivery_Person=1, Order_Address=order_address,
              Order_Postal_Code=postal_code, Order_Time=datetime.now(), Order_Price=order_price, Delivered=False)
    session.add(order)
    increase_pizzas_ordered(session, customer_id)
    session.commit()
    order_item(session, order.Order_ID, item_id, quantity)
    return order.Order_ID

def order_item(session, order_id:int, item_id: int, quantity: int):
    item_ordered = OrderItemLink(Order_ID=order_id, Item_ID=item_id, Quantity=quantity)
    session.add(item_ordered)
    session.commit()

def increase_pizzas_ordered(session, customer_id: int):
    customer = session.query(Customer).filter(Customer.Customer_ID == customer_id).one()
    customer.Pizzas_Ordered += 1

def apply_discount(session, order_price: int, discount_code: int):
    discount = session.query(Discount).filter(Discount.Discount_Code == discount_code).one()
    if discount.Redeemed is False:
        order_price -= (order_price * discount.Percent) / 100
        discount.Redeemed = True
    session.commit()
    return order_price

def loyalty_discount(session, customer_id: int, order_price: int):
    customer = session.query(Customer).filter(Customer.Customer_ID == customer_id).one()
    if customer.Pizzas_Ordered % 10:
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
            if 0 < item.item_id <= 10:
                cheapest_pizza = min(cheapest_pizza, item.Item_Price)
            elif 10 < item.item_id <= 20:
                cheapest_drink = min(cheapest_drink, item.Item_Price)

        print("It's your Birthday! You received only the cheapest items for free as we need as much profit as possible.")
        return order_price - cheapest_drink - cheapest_pizza

    return order_price

def checkout(session, order_id: int, discount_code: int):
    items = session.query(OrderItemLink).filter(OrderItemLink.Order_ID == order_id).all()
    order = session.query(Order).filter(Order.Order_ID == order_id).one()
    price = 0
    for item in items:
        if 0 < item.item_id <= 10:
            price += (calculate_price(session,item.item_id) * item.Quantity)
        else:
            price += (item.Item_price * item.Quantity)
    if discount_code is not None:
        order.Discount_Code = discount_code
        total_price = apply_discount(session, price, discount_code)
    else:
        total_price = price
    print(f"Total price: {total_price}" +
          "\nThank you for your order!" +
          "\nWe hope to see you again soon!")