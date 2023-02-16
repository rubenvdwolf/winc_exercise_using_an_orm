import peewee

db = peewee.SqliteDatabase(":memory:")


class Ingredient(peewee.Model):
    name = peewee.CharField()
    is_vegetarian = peewee.BooleanField()
    is_vegan = peewee.BooleanField() # added by me
    is_glutenfree = peewee.BooleanField()

    class Meta:
        database = db


class Restaurant(peewee.Model):
    name = peewee.CharField()
    open_since = peewee.DateField() # added by me
    opening_time = peewee.TimeField() # added by me
    closing_time = peewee.TimeField()

    class Meta:
        database = db


class Dish(peewee.Model):
    name = peewee.CharField() # added by me
    served_at = peewee.ForeignKeyField(Restaurant)
    price_in_cents = peewee.DecimalField(decimal_places=2) # added by me
    ingredients = peewee.ManyToManyField(Ingredient)

    class Meta:
        database = db


class Rating(peewee.Model):
    restaurant = peewee.ForeignKeyField(Restaurant)
    rating = peewee.IntegerField() # added by me
    comment = peewee.CharField(null=True)

    class Meta:
        database = db


DishIngredient = Dish.ingredients.get_through_model()