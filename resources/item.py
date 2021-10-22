
# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.itemmodel import ItemModel

class ItemList(Resource):
    def get(self):
        # return {'items': ItemModel.query.all()}
        return {'items': [item.json() for item in ItemModel.query.all()]}   # list comprehension way

        # lambda option for above

        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}   # lambda way


class Item(Resource):  # create a class called Student and inherit the Resource class.

    parser = reqparse.RequestParser()  # creates a new parser object - reminds me of argparse, but this is for requests.
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")


    # commented out because auth stopped working. @jwt_required()        # this forces you to have a JWT authorization key.
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()  # we cant return an object to the get command.

        return {'message': 'Item not found'}, 404



    def post(self, name):  #  create items

        if ItemModel.find_by_name(name):
            return {'message': "an item with name '{}' already exists.".format(name)}, 400  # bad request

        data = Item.parser.parse_args()  # refer to teh parser defined at the class level above.
        # item = {'name': name, 'price': data['price']}
        item = ItemModel(name, data['price'], data['store_id'])   # now returns an object instead of a dictionary item.
        #  item = ItemModel(name, **data)  # he says that this will work, but it is just ugly IMHO
        try:
            item.save_to_db()
        except:
            return{"message": "an error occurred during the insert"}, 500 # internal server error.

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item Deleted'}

    def put(self, name):  # will update or create a new item.
        data = Item.parser.parse_args()  # refer to teh parser defined at the class level above.
        item = ItemModel.find_by_name(name)

        if item is None:   # create a new item
            try:
                item = ItemModel(name, data['price'], data['store_id'])
            except:
                return {"message": " Error inserting new item"}, 500
        else:
            try:
                item.price = data['price']
                item.store_id = data['store_id']  # Not part of video, but told us we could so this too.
            except:
                return {"Message": " Error updating item "}, 500
        item.save_to_db()  # this will update or insert as needed.
        return item.json()


