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

def new_order(session,customer_id: int, discount_code: int, order_address: str, pizza_id: int, ):


