#!/usr/bin/env python3

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
import os


from app.models import db

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] ="postgresql://restaurant_pizza_db_rlbf_user:C1nXIQ1bb5cWlYTOjodpl1bTiLyQW7ye@dpg-ckcqgi4iibqc73dq9it0-a.oregon-postgres.render.com/restaurant_pizza_db_rlbf"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# db.init_app(app)
# migrate = Migrate(app, db)

# api = Api(app)

# # from api import routes

# from flask import Flask
# from flask_restful import Api
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurant.db'


db.init_app(app)
migrate = Migrate(app, db)


api = Api(app)
