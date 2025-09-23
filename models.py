from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)

    orders = db.relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.id} {self.email}>"

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)

    items = db.relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product {self.id} {self.name} {self.price}>"

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    @property
    def total(self):
        return round(sum(i.quantity * i.unit_price for i in self.items), 2)

    @property
    def item_count(self):
        return sum(i.quantity for i in self.items)

    def __repr__(self):
        return f"<Order {self.id} user={self.user_id}>"

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="items")

    def __repr__(self):
        return f"<OrderItem order={self.order_id} product={self.product_id} qty={self.quantity}>"

def seed_data():
    if User.query.count() == 0:
        db.session.add_all([
            User(name="Ada Lovelace", email="ada@example.com"),
            User(name="Grace Hopper", email="grace@example.com"),
            User(name="Edsger Dijkstra", email="edsger@example.com"),
        ])
    if Product.query.count() == 0:
        db.session.add_all([
            Product(name="Coffee Beans 250g", price=9.95),
            Product(name="Espresso Cup", price=5.50),
            Product(name="French Press", price=24.90),
        ])
    db.session.commit()
