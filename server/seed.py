#!/usr/bin/env python3

from faker import Faker
from app.models import db, Restaurant, Pizza, RestaurantPizza
from app.app import app
import random


with app.app_context():
    fake = Faker()

    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()

    restaurants = []
    restaurant_names = ["Krusty Krab","The Chum Bucket","Ichiraku Ramen","Bob's Burgers",
                   "The Drunken Clam","Pizza Planet","The Krusty Burger",
                   "Cafe Nowhere","Baratie","Nekoya","WcDonald's"]

    for restaurant in restaurant_names:
        new_restaurant = Restaurant(
            name = restaurant,
            address = fake.address()
        )
        restaurants.append(new_restaurant)
    db.session.add_all(restaurants)
    db.session.commit()


    pizzas = []
    pizza_names = ["Krabby Patty","Seafoam Supreme ","Anchovy ","Bob's Special"
                   ,"Tina's Twisted","Louise's Luscious","Space Explorer","Alien Supreme"
                   ,"Rocket Fuel Pepperoni","Naruto Special","Hokage's Hawaiian",
                   "Sasuke's Sharingan Sausage","Big Mac","Chicken McNugget","Happy Meal"
                   ,"Margherita","Pepperoni","Supreme","Hawaiian","Vegetarian",
                   "Meat Lovers","BBQ Chicken","Mushroom and Olive","Buffalo Chicken","Four Cheese"]
    for pizza in pizza_names:
        new_pizza = Pizza(
            name = pizza,
            ingredients = ', '.join([' '.join(fake.words(3)) for _ in range(7)]),
        )
        pizzas.append(new_pizza)
    db.session.add_all(pizzas)
    db.session.commit()

    restaurant_pizzas = []
    for restaurant in restaurants:
        for pizza in pizzas:
            new_restaurant_pizza = RestaurantPizza(
                pizza_id=pizza.id,
                restaurant_id=restaurant.id,
                price=round(random.uniform(1.33, 29.66), 2)
            )    
            restaurant_pizzas.append(new_restaurant_pizza)
    db.session.add_all(restaurant_pizzas)
    db.session.commit()