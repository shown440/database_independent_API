from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel
from db import db

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message":"{} store is not found".format(name)}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message":"{} store is already exist.".format(name)}, 400

        sql = db.text('SELECT (NVL(MAX(ID),0)+1) FROM STORES6')
        my_store_id = db.engine.execute(sql).fetchone()

        store = StoreModel(my_store_id[0], name)
        try:
            store.save_to_db()
        except Exception as e:
            return {"message":"Unexpected error occured in Stroe insertion. please see the post method of store Resource."}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message":"{} store is deleted successfully.".format(name)}
        else:
            return {"message":"{} store unable to delete.".format(name)}


class StoreList(Resource):
    def get(self):
        return {"store":[store.json() for store in StoreModel.query.all()]}
