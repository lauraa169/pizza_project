# README: this file contains all the application logic
# such as displaying menu, placing orders(??), etc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers import is_vegan_pizza
from models import Base, seed_data, MenuItem, Pizza

def display_menu_orm(session):
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
        vegetarian_badge = " (vegetarian)" if bool(pi.Vegetarian_Pizza) else "" #TODO
        pizza_price = # calculate price
        print(f"{pi.Pizza_ID} | {pi.Pizza_Name}{vegan_badge} {vegetarian_badge}.......... {pizza_price}")

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

def populate_vegan(session):
    pizzas = session.query(Pizza).all()
    for p in pizzas:
        p.Vegan_Pizza = is_vegan_pizza(session, p.Pizza_ID)
    session.commit()

def main():
    engine = create_engine("sqlite:///app.db", echo=False, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    with Session() as session:
        seed_data(session)
        populate_vegan(session)
        display_menu_orm(session)

if __name__ == "__main__":
    main()

