#import sqlite3
#import cx_Oracle

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel
from db import db

###############################################################################
###############################################################################
##### SQLite3 DB Item(Resource) ###############################################
###############################################################################
###############################################################################

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

        item = ItemModel(item_id[0], name, data["price"], data["store_id"]) #ItemModel(name, data["price"]) <- {"name":name, "price":data["price"]}
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

#################################################################################
#################################################################################
##### ORACLE DB Item(Resource) ##################################################
#################################################################################
################################################################################

# class Item(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument("price",
#         type=float,
#         required=True,
#         help="Field can't be empty..."
#     )
#
#     @classmethod
#     def find_by_name(cls, name):
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#
#         # int=INTEGER. but if we need auto incremented id then we have to write INTEGER
#         query = "SELECT * FROM REST_ITEMS WHERE name=:name"
#         result = cursor.execute(query, (name,))
#         row = result.fetchone()
#
#         connection.close()
#         if row:
#             return {"item":{"name":row[0], "price":row[1]}}, 200
#
#     @jwt_required()
#     def get(self, name):
#         item = self.find_by_name(name)
#         if item:
#             return item
#         return {"message":"{} is not found".format(name)}, 404
#
#     @classmethod
#     def insert(cls, item):
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#
#         query="INSERT INTO REST_ITEMS VALUES(:1, :2)"
#         cursor.execute(query, (item["name"], item["price"], ))
#
#         connection.commit()
#         connection.close()
#
#     def post(self, name):
#         if self.find_by_name(name):
#             return {"Message":"{} is exist. No need to create it again.".format(name)}, 400
#
#         data = Item.parser.parse_args()
#         item = {"name":name, "price":data["price"]}
#
#         try:
#             self.insert(item)
#         except:
#             return {"message":"{} insertion failed.".format(name)}, 500
#         return item, 201
#
#
#     def delete(self, name):
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#
#         query="DELETE FROM REST_ITEMS WHERE name=:name"
#         cursor.execute(query, (name, ))
#
#         connection.commit()
#         connection.close()
#         return {"message" : "Item {} deleted successfully".format(name)}
#
#     @classmethod
#     def update(cls, item):
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#
#         query="UPDATE REST_ITEMS SET price=:1 WHERE name=:2"
#         cursor.execute(query, (item["price"], item["name"], ))
#
#         connection.commit()
#         connection.close()
#
#     def put(self, name):
#         data = Item.parser.parse_args()
#
#         item_exist = self.find_by_name(name)
#         update_item = {"name":name, "price":data["price"]}
#         if item_exist is None: # is None
#             try:
#                 self.insert(update_item)
#             except:
#                 return {"message":"Updating error. Please see the update and put method."}, 500
#         else:
#             try:
#                 self.update(update_item)
#             except:
#                 return {"message":"Updating error. Please see the update and put method."}, 500
#         return update_item
#
# class ItemList(Resource):
#     #@jwt_required()
#     def get(self):
#         items = []
#
#         connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
#         cursor = connection.cursor()
#         query="SELECT * FROM REST_ITEMS"
#         result = cursor.execute(query)
#
#         for row in result:
#             items.append({"name":row[0], "price":row[1]})
#
#         connection.close()
#         return {"items" : items}
