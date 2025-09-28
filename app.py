# README: this file contains all the application logic
# such as displaying menu, placing orders(??), etc

from flask import Flask
from controllers import customers_bp, orders_bp, products_bp, is_vegan_pizza
from models import db, seed_data, MenuItem, Pizza

# this is a helper function
def display_menu_orm():
    # Must be called within app.app_context()

    # Fetch pizzas with their Vegan_Pizza flag
    pizzas = Pizza.query.order_by(Pizza.Pizza_ID).all()

    # Fetch all menu items for drinks and desserts printing
    items = MenuItem.query.order_by(MenuItem.Item_ID).all()

    print("Menu Items:")
    print("----------")
    print("ID | Name | Price")
    print("----------")

    # simple line printer for non-pizza items
    def line_item(mi):
        print(f"{mi.Item_ID} | {mi.Item_Name} .......... {mi.Item_Price}")

    # pizza printer with vegan badge
    def line_pizza(pi):
        vegan_badge = " (vegan)" if bool(pi.Vegan_Pizza) else ""
        print(f"{pi.Pizza_ID} | {pi.Pizza_Name}{vegan_badge} .......... {pi.Pizza_Price}")

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

def populate_vegan():
    # checks if pizzas need to be updated to vegan
    needs_update = Pizza.query.filter(Pizza.Vegan_Pizza.is_(None)).count() > 0
    if not needs_update:
        return
    pizzas = Pizza.query.all()
    for p in pizzas:
        p.Vegan_Pizza = is_vegan_pizza(p.Pizza_ID)
    db.session.commit()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "dev-secret"

    db.init_app(app)

    app.register_blueprint(customers_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(products_bp)

    with app.app_context():
        # creates db
        db.create_all()
        # populates data
        seed_data()
        # labels pizzas as vegan
        populate_vegan()
        # displays menu
        display_menu_orm()

    @app.route("/")
    def index():
        return (
            "<h3>Flask MVC + SQLAlchemy ORM</h3>"
            '<p>See <a href="/users">/users</a>, '
            '<a href="/products">/products</a>, '
            'and <a href="/orders">/orders</a>.</p>'
        )

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
