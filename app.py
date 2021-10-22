import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity  # in our next py file that we created.
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')  #IF THE DATABASE_URL is not found, then use sqllite
#app.config['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns off the flask sqlaclchemy transaction tracking, but leaves sqlalchemy on..
app.secret_key = 'Henry'
api = Api(app)


jwt = JWT(app, authenticate, identity)  # creates /auth

api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items/')
api.add_resource(UserRegister,'/register')


if __name__ == '__main__':  # forces this to ONLY run if we run this file. Not if this is imported into another file.
    db.init_app(app)    # see app defined above.
    app.run(port=5000, debug=True)  # not really needed, the default port is 5000, but its nice to be sure.