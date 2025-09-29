# README: this file contains all the application logic
# such as displaying menu, placing orders(??), etc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers import *
from models import Base, seed_data, MenuItem, Pizza

def display_menu(session):
    pizzas = session.query(Pizza).order_by(Pizza.Pizza_ID).all()
    items = session.query(MenuItem).order_by(MenuItem.Item_ID).all()

    print("Menu Items:")
    print("----------")
    print("ID | Name | Price")
    print("----------")

    def line_item(mi):
        print(f"{mi.Item_ID} | {mi.Item_Name} .......... {mi.Item_Price}")

    def line_pizza(pi):
        vegan_badge = " (vegan)" if bool(pi.Vegan_Pizza) else ""
        vegetarian_badge = " (vegetarian)" if bool(pi.Vegetarian_Pizza) else ""

        print(f"{pi.Pizza_ID} | {pi.Pizza_Name}{vegan_badge}{vegetarian_badge}.......... {calculate_price(session, pi.Pizza_ID)}")

    print("Pizzas:")
    for pi in pizzas:
        line_pizza(pi)
    print("----------")

    print("Drinks:")
    for mi in items[10:20]:
        line_item(mi)
    print("----------")

    print("Desserts:")
    for mi in items[20:30]:
        line_item(mi)

    continue_message(session)

def populate_vegan(session):
    pizzas = session.query(Pizza).all()
    for p in pizzas:
        p.Vegan_Pizza = is_vegan_pizza(session, p.Pizza_ID)
    session.commit()

def populate_vegetarian(session):
    pizzas = session.query(Pizza).all()
    for p in pizzas:
        p.Vegetarian_Pizza = is_vegetarian_pizza(session, p.Pizza_ID)
    session.commit()

def start(session):
    print("Welcome to Onsen Pizza!" +
          "\nWith good pizza and even better coffee :)")
    customer_input(session)

def continue_message(session):
    print("\n ------------------------------------------------")
    answer = str(input("\nWould you like to continue (y/n)? "))
    if answer == "y":
        customer_input(session)
    elif answer == 'n':
        exit(0)
    else:
        print("Please use the correct input.")
        continue_message(session)

def customer_input(session):
        print("\n ------------------------------------------------" +
        "\n| Press 1 to display the menu.                   |" +
        "\n| Press 2 to place an order.                     |" +
        "\n| Press 3 to create an account.                  |" +
        "\n| Press 4 to exit.                               |" +
        "\n ------------------------------------------------")
        answer = int(input("\nWhat would you like to do? "))
        if answer == 1:
            display_menu(session)
        elif answer == 2:
            place_order(session)

def place_order(session):
    print("\nPlease enter your order details.")
    customer_id = int(input("Customer ID: "))
    pizza_id = int(input("Pizza ID (1 - 10): "))
    pizza_quantity = int(input("Pizza Quantity: "))
    order_address = input("Order Address: ")
    postal_code = input("Order Postal Code: ")
    order_price = calculate_price(session, pizza_id) * pizza_quantity
    order_id = new_order(session, customer_id, pizza_id, pizza_quantity, order_address, postal_code, order_price)
    answer = int(input("Would you like to order another pizza?" +
          "\nPress 1 for yes or 2 for no."))
    if answer == 1:
        order_extra_item(session, order_id)
    print(f"\nOrder placed successfully! Your total price is: {order_price}")
    continue_message(session)

def order_extra_item(session, order_id: int):
    item_id = int(input("Enter the number of the item you want to order:"))
    quantity = int(input("How many would you like to order?"))
    order_item(session, order_id, item_id, quantity)
    print(f"\nItem ordered successfully!")
    answer = int(input("Would you like to order another pizza?" +
                       "\nPress 1 for yes or 2 for no."))
    if answer == 1:
        order_extra_item(session, order_id)
    elif answer == 2:
        checkout_page(session, order_id)
    session.commit()

def checkout_page(session, order_id: int):
    discount_code = int(input("Discount code (optional): "))
    checkout(session, order_id, discount_code)
    print(f"\nCheckout complete!")
    continue_message(session)

def main():
    engine = create_engine("sqlite:///app.db", echo=False, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    with Session() as session:
        seed_data(session)
        populate_vegan(session)
        populate_vegetarian(session)
        start(session)

if __name__ == "__main__":
    main()
