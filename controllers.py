# README: this file contains all the business logic for the app
# such as how we define vegan and vegetarian pizzas, how we calculate prices, etc.

from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import selectinload
from models import *


orders_bp = Blueprint("orders", __name__)
products_bp = Blueprint("products", __name__)

customers_bp = Blueprint("customers", __name__)

ingredients_bp = Blueprint("ingredients", __name__)

pizzas_bp = Blueprint("pizzas", __name__)

drinks_bp = Blueprint("drinks", __name__)

desserts_bp = Blueprint("desserts", __name__)


def is_vegan_pizza(pizza_id: int) -> bool:
    # Join Pizza_Ingredient -> Ingredient and check if any ingredient is non-vegan
    non_vegan_exists = (
        db.session.query(Ingredient)
        .join(PizzaIngredient, Ingredient.Ingredient_ID == PizzaIngredient.c.Ingredient_ID)
        .filter(PizzaIngredient.c.Pizza_ID == pizza_id, Ingredient.Vegan_Ingredient.is_(False))
        .first()
        is not None
        # returns true if the pizza contains a non-vegan ingredient
    )
    # returns True if no non-vegan ingredients
    return not non_vegan_exists


# Orders
@orders_bp.route("/orders")
def list_orders():
    # Eager load user and items->product to avoid N+1
    orders = (Order.query
              .options(selectinload(Order.user),
                       selectinload(Order.items).selectinload(OrderItemLink.product))
              .order_by(Order.id)
              .all())
    return render_template("orders.html", title="Orders", orders=orders)

@orders_bp.route("/orders/new")
# THIS NEEDS TO CHANGE, IT IS PART OF THE TEMPLATE, NOT COMPATIBLE W OUR DB
def new_order():
    customers = Customer.query.order_by(Customer.name).all()
    products = Product.query.order_by(Product.name).all()
    return render_template("order_form.html", title="New Order", users=users, products=products)

@orders_bp.route("/orders", methods=["POST"])
def create_order():
    customer_id = request.form.get("customer_id")
    product_id = request.form.get("product_id")
    qty = request.form.get("qty", "1")
    try:
        qty = int(qty)
    except:
        qty = 1
    user = Customer.query.get(customer_id)
    product = Product.query.get(product_id)
    if not user or not product:
        flash("Please select a valid user and product.", "error")
        return redirect(url_for("orders.new_order"))
    order = Order(user=user)
    db.session.add(order)
    db.session.flush()  # get order.id
    db.session.add(OrderItem(order_id=order.id, product_id=product.id, quantity=qty, unit_price=product.price))
    db.session.commit()
    flash("Order created.", "success")
    return redirect(url_for("orders.list_orders"))
