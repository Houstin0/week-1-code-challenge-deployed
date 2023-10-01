#!/usr/bin/env python3

from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


db=SQLAlchemy()

class Restaurant(db.Model,SerializerMixin):
    __tablename__="restaurants"

    

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True)
    address=db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurants', overlaps="restaurant_pizza")
    pizzas = db.relationship('Pizza', secondary='restaurant_pizzas', back_populates='restaurants',overlaps="restaurant_pizzas")

    serialize_rules = ('-restaurant_pizzas','-pizzas' )

    def __repr__(self):
        return f'< Restaurant {self.name} | Address: {self.address}>'
    
    @validates('name')
    def check_name(self,key,name):
        if len(name) > 50:
            raise ValueError("Name must be less than 50 words in length.",403)
        return name

    
class Pizza(db.Model,SerializerMixin):
    __tablename__="pizzas"   

   

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    ingredients=db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizzas',overlaps="pizzas")
    restaurants = db.relationship('Restaurant', secondary='restaurant_pizzas', back_populates='pizzas',overlaps="restaurant_pizzas")
    
    serialize_rules = ('-restaurant_pizzas','-restaurants') 
    
    def __repr__(self):
        return f'< Pizza {self.name} | Ingredients: {self.ingredients}>'
    
class RestaurantPizza(db.Model,SerializerMixin):
    __tablename__="restaurant_pizzas"

    

    id=db.Column(db.Integer,primary_key=True)
    pizza_id=db.Column(db.Integer,db.ForeignKey("pizzas.id"))
    restaurant_id=db.Column(db.Integer,db.ForeignKey("restaurants.id"))
    price=db.Column(db.Float) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    pizzas = db.relationship('Pizza', back_populates='restaurant_pizzas',overlaps="pizzas,restaurants")
    restaurants = db.relationship('Restaurant', back_populates='restaurant_pizzas',overlaps="pizzas,restaurants")
    
    serialize_rules = ('-pizzas', '-restaurants')

    def __repr__(self):
        return f'< Restaurant Pizza Price {self.price} | Created at: {self.created_at} | Updated at: {self.updated_at} >'
    
    @validates('price')
    def check_price(self, key, price):
        if 1 <= price <= 30:
            return price
        else:
            raise ValueError("Price must be between 1 and 30",403)

    