from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel


class ItemList(Resource):

    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True, type=float, help="this can't be blank")
    # parser.add_argument('name', required=True, type=str, help="this field can't be blank")
    parser.add_argument('store_id', required=True, type=int, help="Every item needs a store id")


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {"message": "An item with this name '{}' already exits".format(name)}, 400

        req_data = Item.parser.parse_args()
        item = ItemModel(name, **req_data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item"}, 500

        return {'message': 'Item created'}, 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}, 202
        return {"message": "item with the name '{}' does not exist".format(name)}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
                item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()
