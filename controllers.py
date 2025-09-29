# README: this file contains all the business logic for the app
# such as how we define vegan and vegetarian pizzas, how we calculate prices, etc.
from sqlalchemy.orm import selectinload
from models import *


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



