#!/usr/bin/env python3

from flask_restful import Resource
from flask import make_response,request,jsonify
from models import Pizza,Restaurant,RestaurantPizza
from app import db
from app import api

class Index(Resource):
    def get(self):
        try:
            response_dict = {
                "index": "Welcome to the Pizza Restaurant RESTful API",
            }
            return make_response(jsonify(response_dict), 200)
            
        except Exception as e:
            response_dict = {"error": "An error occurred."}
            return make_response(jsonify(response_dict), 500)

api.add_resource(Index, '/')

class Restaurants(Resource):
    def get(self):
        try:
            restaurants_dicts = []
            for restaurant in Restaurant.query.all():
                restaurant_dict = restaurant.to_dict()
                restaurants_dicts.append(restaurant_dict)

            return make_response(jsonify(restaurants_dicts),200)
        
        except Exception:
            response_dict = {"error": "An error occurred while fetching restaurants."}
            return make_response(jsonify(response_dict), 500)

    
    def post(self):
        data = request.get_json()
        try:
            new_restaurant=Restaurant(
                name=data.get("name"),
                address=data.get("address")
            )
            db.session.add(new_restaurant)
            db.session.commit()

            return make_response(jsonify(new_restaurant.to_dict()), 201)
        
        except Exception as e:
            response_dict = {"error": f"{str(e)}"}
            return make_response(jsonify(response_dict), 403)

api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):
    def get(self, id):
        try:
            restaurant = Restaurant.query.filter_by(id=id).first()
            if restaurant:
                response_dict = {
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "address": restaurant.address,
                    "pizzas": [pizza.to_dict() for pizza in restaurant.pizzas]
                }
                return make_response(jsonify(response_dict), 200)
                
            else:
                response_dict = {"error": "Restaurant not found"}
                return make_response(jsonify(response_dict), 404)
            
        except Exception as e:
            response_dict = {"error": "An error occurred while fetching restaurant by ID."}
            return make_response(jsonify(response_dict), 500)

    def patch(self,id):
        data = request.get_json()
        try:
            restaurant= Restaurant.query.filter_by(id=id).first()

            for attr in data:
                setattr(restaurant,attr,data.get(attr))

            db.session.add(restaurant)
            db.session.commit()

            response_dict=restaurant.to_dict()
            return make_response(jsonify(response_dict),200)    
            
        except Exception as e:
            response_dict = {"error": "An error occurred while updating the restaurant."}
            return make_response(jsonify(response_dict), 500)
        
    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        try:
            if restaurant:
                for restaurant_pizza in restaurant.restaurant_pizzas:
                    db.session.delete(restaurant_pizza)
                db.session.delete(restaurant)
                db.session.commit()

                return make_response('Restaurant deleted successfully', 204)
            else:
                response_dict = {"error": "Restaurant not found"}
                return make_response(jsonify(response_dict), 404)
            
        except Exception as e:
            response_dict = {"error": f"An error occurred while deleting the restaurant: {str(e)}"}
            return make_response(jsonify(response_dict), 500)
        
api.add_resource(RestaurantByID, '/restaurants/<int:id>')

class Pizzas(Resource):
    def get(self):
        try:
            pizzas = Pizza.query.all()
            pizzas_dicts = [pizza.to_dict() for pizza in pizzas]
            return make_response(jsonify(pizzas_dicts), 200)
    
        except Exception as e:
            response_dict = {"error": "An error occurred while fetching pizzas."}
            return make_response(jsonify(response_dict), 500)
    
    def post(self):
        data=request.get_json()
        try:
            new_pizza=Pizza(
                name=data.get("name"),
                ingredients=data.get("ingredients")
            )
            db.session.add(new_pizza)
            db.session.commit()

            return make_response(jsonify(new_pizza.to_dict()),201)
        
        except Exception as e:
            response_dict = {"error": "An error occurred while creating a new pizza."}
            return make_response(jsonify(response_dict), 500)




api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):
    def get(self):
        try:
            restaurants_pizzas_dicts = []
            for restaurant_pizza in RestaurantPizza.query.all():
                restaurant_dict = restaurant_pizza.to_dict()
                restaurants_pizzas_dicts.append(restaurant_dict)
            return make_response(jsonify(restaurants_pizzas_dicts), 200)
            
        
        except Exception as e:
            response_dict = {"error": "An error occurred while fetching restaurant pizzas."}
            return make_response(jsonify(response_dict), 500)

     
    def post(self):
        data = request.get_json()
        try:
            new_restaurant_pizza=RestaurantPizza(
                price=data.get('price'),
                pizza_id= data.get("pizza_id"),
                restaurant_id= data.get("restaurant_id"),
            ) 
            db.session.add(new_restaurant_pizza)
            db.session.commit()
        
            response = make_response(
                new_restaurant_pizza.to_dict(),
                201 
            )
            return response
        
        except Exception as e:
            response_dict = {"error" : f"{str(e)}"}
            return make_response(jsonify(response_dict), 403)

    
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')