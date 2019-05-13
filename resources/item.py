#import sqlite3
#import cx_Oracle

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel
from db import db


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="Field can't be empty..."
    )
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every items need a store id."
    )

    #@jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name) # here we pass the name into ItemModel calss of item.py in models packageand it return value as object
        if item:
            return item.json()
        return {"message":"{} is not found".format(name)}, 404

    #@jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name): # here we pass the name into ItemModel calss of item.py in models package and it return value as object
            return {"Message":"{} is exist. No need to create it again.".format(name)}, 400

        data = Item.parser.parse_args()
        #print("####################", data)
        sql = db.text('SELECT (NVL(MAX(ID),0)+1) FROM ITEMS6')
        item_id = db.engine.execute(sql).fetchone()

        item = ItemModel(item_id[0], name, data["price"], data["store_id"]) #item_id[0] *** #ItemModel(name, data["price"]) <- {"name":name, "price":data["price"]}
        #because this is not a dictionary. Its a ItemModel object now.

        try:
            item.save_to_db() #now we directly insert item because item is now ItemModel class object. #ItemModel.insert(item)
        except:
            return {"message":"{} insertion failed.".format(name)}, 500
        return item.json(), 201

    #@jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message" : "Item {} deleted successfully".format(name)}

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name) # here we pass the name into ItemModel calss of item.py in models package and it return value as object

        if item is None: # is None
            try:
                item = ItemModel(name, data["price"], data["store_id"]) #ItemModel.insert(update_item) ##data["price"], data["store_id"]=**data
            except:
                return {"message":"Updating error. Please see the update and put method."}, 500
        else:
            try:
                item.price = data["price"]
            except:
                return {"message":"Updating error. Please see the update and put method."}, 500

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    #@jwt_required()
    def get(self):
        #"item"=[items json() here]
        return {"items" :[x.json() for x in ItemModel.query.all()]}
        #return {"items" :list(map(lambda x : x.json(), ItemModel.query.all()))}
