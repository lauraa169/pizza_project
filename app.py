from flask import Flask
from controllers import users_bp, orders_bp, products_bp
from models import db, seed_data

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "dev-secret"

    db.init_app(app)

    app.register_blueprint(users_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(products_bp)

    with app.app_context():
        db.create_all()
        seed_data()

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
