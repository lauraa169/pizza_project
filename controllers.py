from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.orm import selectinload
from models import db, User, Product, Order, OrderItem

users_bp = Blueprint("users", __name__)
orders_bp = Blueprint("orders", __name__)
products_bp = Blueprint("products", __name__)

# Users
@users_bp.route("/users")
def list_users():
    users = User.query.order_by(User.id).all()
    return render_template("users.html", title="Users", users=users)

@users_bp.route("/users/new")
def new_user():
    return render_template("user_form.html", title="New User", user=None)

@users_bp.route("/users", methods=["POST"])
def create_user():
    name = request.form.get("name","").strip()
    email = request.form.get("email","").strip()
    if not name or not email:
        flash("Name and email are required.", "error")
        return redirect(url_for("users.new_user"))
    db.session.add(User(name=name, email=email))
    db.session.commit()
    flash("User created.", "success")
    return redirect(url_for("users.list_users"))

# Products
@products_bp.route("/products")
def list_products():
    products = Product.query.order_by(Product.id).all()
    return render_template("products.html", title="Products", products=products)

@products_bp.route("/products/new")
def new_product():
    return render_template("product_form.html", title="New Product", product=None)

@products_bp.route("/products", methods=["POST"])
def create_product():
    name = request.form.get("name","").strip()
    price = request.form.get("price","").strip()
    try:
        price = float(price)
    except:
        flash("Price must be a number.", "error")
        return redirect(url_for("products.new_product"))
    if not name:
        flash("Name is required.", "error")
        return redirect(url_for("products.new_product"))
    db.session.add(Product(name=name, price=price))
    db.session.commit()
    flash("Product created.", "success")
    return redirect(url_for("products.list_products"))

# Orders
@orders_bp.route("/orders")
def list_orders():
    # Eager load user and items->product to avoid N+1
    orders = (Order.query
              .options(selectinload(Order.user),
                       selectinload(Order.items).selectinload(OrderItem.product))
              .order_by(Order.id)
              .all())
    return render_template("orders.html", title="Orders", orders=orders)

@orders_bp.route("/orders/new")
def new_order():
    users = User.query.order_by(User.name).all()
    products = Product.query.order_by(Product.name).all()
    return render_template("order_form.html", title="New Order", users=users, products=products)

@orders_bp.route("/orders", methods=["POST"])
def create_order():
    user_id = request.form.get("user_id")
    product_id = request.form.get("product_id")
    qty = request.form.get("qty", "1")
    try:
        qty = int(qty)
    except:
        qty = 1
    user = User.query.get(user_id)
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
