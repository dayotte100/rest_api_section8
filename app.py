from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity  # in our next py file that we created.
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # sqlite can also be oracle mysql and others I guess.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns off the flask sqlaclchemy transaction tracking, but leaves sqlalchemy on..
app.secret_key = 'Henry'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()    # this will create the data.db file - no need for create tables dot py.  it must see them in an import definition.

jwt = JWT(app, authenticate, identity)  # creates /auth

api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items/')
api.add_resource(UserRegister,'/register')


if __name__ == '__main__':  # forces this to ONLY run if we run this file. Not if this is imported into another file.
    db.init_app(app)    # see app defined above.
    app.run(port=5000, debug=True)  # not really needed, the default port is 5000, but its nice to be sure.