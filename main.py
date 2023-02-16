import models
import peewee
from typing import List
from datetime import time

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def cheapest_dish() -> models.Dish:
    """You want ot get food on a budget

    Query the database to retrieve the cheapest dish available
    """
    return models.Dish.select().order_by(models.Dish.price_in_cents).first()


def vegetarian_dishes() -> List[models.Dish]:
    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """
    vegetarian_dishes = []
    for dish in models.Dish.select():
        ingreds = []
        for ingredient in dish.ingredients:
            ingreds.append(ingredient.is_vegetarian)
        if all(ingreds):
            vegetarian_dishes.append(dish)
    return vegetarian_dishes


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """
    average_rating_query = (
        models.Rating
        .select(models.Rating.restaurant, peewee.fn.AVG(models.Rating.rating).alias('avg_rating'))
        .group_by(models.Rating.restaurant)
        .alias('avg_ratings')
    )
    query = (
        models.Restaurant
        .select()
        .join(average_rating_query)
        .where(models.Restaurant.id == average_rating_query.c.restaurant)
        .order_by(average_rating_query.c.avg_rating.desc())
    )
    return query.first()


def add_rating_to_restaurant() -> None:
    """After visiting a restaurant, you want to leave a rating

    Select the first restaurant in the dataset and add a rating
    """
    restaurant = models.Restaurant.get(models.Restaurant.id == 1)
    rating = 5
    comment = 'Great little restaurant'
    models.Rating.create(restaurant=restaurant, rating=rating, comment=comment)


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """
    # Get restaurants open > 19.00, get Dishes served at those restaurants, check if they are vegan. If vegan, add restaurant to list.
    open_restaurants = models.Restaurant.select().where(models.Restaurant.closing_time > peewee.TimeField(time(19, 00)))
    open_restautant_with_vegan = []
    for open_restaurant in open_restaurants:
        vegan_dishes = []
        for dish in models.Dish.select().where(models.Dish.served_at == open_restaurant):
            ingreds = []
            for ingredient in dish.ingredients:
                ingreds.append(ingredient.is_vegan)
            if all(ingreds):
                vegan_dishes.append(dish)
        if len(vegan_dishes) != 0:
            open_restaurant_with_vegan.append(open_restaurant)
    return open_restautant_with_vegan

def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    #dish name = tosti, ingredients = cheese, bread, butter
    dish_name = 'Tosti'
    restaurant = models.Restaurant.get_by_id(1)
    price_in_cents = 500

    ingredients = [['cheese', True, False, True], ['bread', True, True, False], ['butter', True, False, True]]
    dish_query = models.Dish.select().where(models.Dish.name == dish_name)
    if dish_query.exists():
        print('Dish already exists!')
    else:
        for ingredient in ingredients:
            ingredient_query = models.Ingredient.select().where(models.Ingredient.name == ingredient[0])
            if ingredient_query.exists():
                pass
            else:
                models.Ingredient.create(name=ingredient[0], is_vegetarian=ingredient[1], is_vegan=ingredient[2], is_glutenfree=ingredient[3])
        
        tosti = models.Dish.create(name=dish_name, served_at=restaurant, price_in_cents=price_in_cents)
        tosti.ingredients.add(['cheese', 'bread', 'butter'])
    
    return models.Dish.select().where(models.Dish.name == 'Tosti')

    
        