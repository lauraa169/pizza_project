# README: this file contains all the application logic
# such as displaying menu, placing orders(??), etc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers import *
from models import Base, seed_data, MenuItem, Pizza

def display_menu(session):
    pizzas = get_pizzas(session)
    items = get_items(session)

    print("\n1Menu Items:")
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

def start(session):
    print('''
                                                                                                                                                                                                                                      
                                                                                                                                                                                                                                  
PPPPPPPPPPPPPPPPP                                                            lllllll  lllllll                                      iiii        PPPPPPPPPPPPPPPPP     iiii                                                      
P::::::::::::::::P                                                           l:::::l  l:::::l                                     i::::i       P::::::::::::::::P   i::::i                                                     
P::::::PPPPPP:::::P                                                          l:::::l  l:::::l                                      iiii        P::::::PPPPPP:::::P   iiii                                                      
PP:::::P     P:::::P                                                         l:::::l  l:::::l                                                  PP:::::P     P:::::P                                                            
  P::::P     P:::::P  eeeeeeeeeeee    ppppp   ppppppppp       eeeeeeeeeeee    l::::l   l::::l    ooooooooooo   nnnn  nnnnnnnn    iiiiiii         P::::P     P:::::Piiiiiii zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz  aaaaaaaaaaaaa   
  P::::P     P:::::Pee::::::::::::ee  p::::ppp:::::::::p    ee::::::::::::ee  l::::l   l::::l  oo:::::::::::oo n:::nn::::::::nn  i:::::i         P::::P     P:::::Pi:::::i z:::::::::::::::zz:::::::::::::::z  a::::::::::::a  
  P::::PPPPPP:::::Pe::::::eeeee:::::eep:::::::::::::::::p  e::::::eeeee:::::eel::::l   l::::l o:::::::::::::::on::::::::::::::nn  i::::i         P::::PPPPPP:::::P  i::::i z::::::::::::::z z::::::::::::::z   aaaaaaaaa:::::a 
  P:::::::::::::PPe::::::e     e:::::epp::::::ppppp::::::pe::::::e     e:::::el::::l   l::::l o:::::ooooo:::::onn:::::::::::::::n i::::i         P:::::::::::::PP   i::::i zzzzzzzz::::::z  zzzzzzzz::::::z             a::::a 
  P::::PPPPPPPPP  e:::::::eeeee::::::e p:::::p     p:::::pe:::::::eeeee::::::el::::l   l::::l o::::o     o::::o  n:::::nnnn:::::n i::::i         P::::PPPPPPPPP     i::::i       z::::::z         z::::::z       aaaaaaa:::::a 
  P::::P          e:::::::::::::::::e  p:::::p     p:::::pe:::::::::::::::::e l::::l   l::::l o::::o     o::::o  n::::n    n::::n i::::i         P::::P             i::::i      z::::::z         z::::::z      aa::::::::::::a 
  P::::P          e::::::eeeeeeeeeee   p:::::p     p:::::pe::::::eeeeeeeeeee  l::::l   l::::l o::::o     o::::o  n::::n    n::::n i::::i         P::::P             i::::i     z::::::z         z::::::z      a::::aaaa::::::a 
  P::::P          e:::::::e            p:::::p    p::::::pe:::::::e           l::::l   l::::l o::::o     o::::o  n::::n    n::::n i::::i         P::::P             i::::i    z::::::z         z::::::z      a::::a    a:::::a 
PP::::::PP        e::::::::e           p:::::ppppp:::::::pe::::::::e         l::::::l l::::::lo:::::ooooo:::::o  n::::n    n::::ni::::::i      PP::::::P           i::::::i  z::::::zzzzzzzz  z::::::zzzzzzzza::::a    a:::::a 
P::::::::P         e::::::::eeeeeeee   p::::::::::::::::p  e::::::::eeeeeeee l::::::l l::::::lo:::::::::::::::o  n::::n    n::::ni::::::i      P::::::::P          i::::::i z::::::::::::::z z::::::::::::::za:::::aaaa::::::a 
P::::::::P          ee:::::::::::::e   p::::::::::::::pp    ee:::::::::::::e l::::::l l::::::l oo:::::::::::oo   n::::n    n::::ni::::::i      P::::::::P          i::::::iz:::::::::::::::zz:::::::::::::::z a::::::::::aa:::a
PPPPPPPPPP            eeeeeeeeeeeeee   p::::::pppppppp        eeeeeeeeeeeeee llllllll llllllll   ooooooooooo     nnnnnn    nnnnnniiiiiiii      PPPPPPPPPP          iiiiiiiizzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz  aaaaaaaaaa  aaaa
                                       p:::::p                                                                                                                                                                                    
                                       p:::::p                                                                                                                                                                                    
                                      p:::::::p                                                                                                                                                                                   
                                      p:::::::p                                                                                                                                                                                   
                                      p:::::::p                                                                                                                                                                                   
                                      ppppppppp                                                                                                                                                                                   
                                                                                                                                                                                                                                  
    ''')
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
        "\n| Press 3 for staff login.                       |" +
        "\n| Press 4 to exit.                               |" +
        "\n ------------------------------------------------")
        answer = int(input("\nWhat would you like to do? "))
        if answer == 1:
            display_menu(session)
        elif answer == 2:
            place_order(session)
        elif answer == 3:
            staff_login(session)
        elif answer == 4:
            exit(0)

def staff_input(session):
    print("\n ------------------------------------------------" +
          "\n| Press 1 to see monthly earnings by gender.     |" +
          "\n| Press 2 to see monthly earnings by postal code.|" +
          "\n| Press 3 to see monthly earnings by age group.  |" +
          "\n| Press 4 to test the application.               |" +
          "\n| Press 5 to exit.                               |" +
          "\n ------------------------------------------------")
    answer = int(input("\nWhat would you like to do? "))
    if answer == 1:
        year = int(input("Enter the year: "))
        month = int(input("Enter the month (1-12): "))
        print("")
        print(monthly_earnings_gender(session, year, month))
        staff_input(session)
    elif answer == 2:
        monthly_earnings_postal(session, input("Enter the postal code: "))
        staff_input(session)
    elif answer == 3:
        print(monthly_earnings_age(session, int(input("Enter the year: ")), int(input("Enter the month (1-12): "))))
        print("")
        staff_input(session)
    elif answer ==4:
        testing(session)
    elif answer == 5:
        start(session)

def staff_login(session):
    print("\nPlease enter the password to login as a staff member.")
    password = input("Password: ")
    if check_password(session, password):
        print("\nWelcome to the staff panel!")
        staff_input(session)

def place_order(session):
    print("\nPlease enter your order details.")
    customer_id = int(input("Customer ID: "))
    pizza_id = int(input("Pizza ID (1 - 10): "))
    pizza_quantity = int(input("Pizza Quantity: "))
    order_address = input("Order Address: ")
    postal_code = input("Order Postal Code: ")
    order_price = calculate_price(session, pizza_id) * pizza_quantity
    order_id = new_order(session, customer_id, pizza_id, pizza_quantity, order_address, postal_code, order_price)
    answer = str(input("\nWould you like to order another item (y/n)? " ))
    if answer == "y":
        order_extra_item(session, order_id)
    elif answer == "n":
        checkout_page(session, order_id)
    print(f"\nOrder placed successfully! Your total price is: {order_price}")
    continue_message(session)

def order_extra_item(session, order_id: int):
    item_id = int(input("Enter the number of the item you want to order: "))
    quantity = int(input("How many would you like to order? "))
    order_item(session, order_id, item_id, quantity)
    # print(f"Item ordered successfully!")
    answer = str(input("\nWould you like to order another item (y/n)? "))
    if answer == "y":
        order_extra_item(session, order_id)
    elif answer == "n":
        checkout_page(session, order_id)
    session.commit()

def checkout_page(session, order_id: int):
    valid_codes = get_valid_codes(session)
    discount_code_raw = input("Discount code (optional): ").strip()

    discount_code: int | None = None
    if discount_code_raw:
        if discount_code_raw.isdigit():
            candidate = int(discount_code_raw)
            if candidate in valid_codes:
                discount_code = candidate

    # Fallback to a known "no discount" code if it exists in DB, else None
    if discount_code is None:
        checkout(session, order_id, None)
    else:
        checkout(session, order_id, discount_code)

    # print(f"Checkout complete!")
    continue_message(session)

def no_driver_available(session):
    print("There is currently no delivery driver available. Please restart the session and try again later :)")
    exit()

def testing(session):
    print("\nWelcome to the testing panel!")
    print("\n ------------------------------------------------" +
          "\n| Press 1 to test pizza labeling.                |" +
          "\n| Press 2 to exit.                               |" +
          "\n ------------------------------------------------")

    answer = int(input("\nWhat would you like to do? "))
    if answer == 1:
        ingredient1 = str(input("Ingredient 1: "))
        ingredient2 = str(input("Ingredient 2: "))
        ingredient3 = str(input("Ingredient 3: "))
        new_pizza(session, ingredient1, ingredient2, ingredient3)
        display_menu(session)
    elif answer == 2:
        start(session)

def main():
    engine = create_engine("sqlite:///app.db", echo=False, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    with Session() as session:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        seed_data(session)
        populate_vegan(session)
        populate_vegetarian(session)
        start(session)

if __name__ == "__main__":
    main()
