#import sqlite3
#import cx_Oracle

from db import db

class ItemModel(db.Model):
    __tablename__ = "items6"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores6.id"))
    store = db.relationship("StoreModel")

    def __init__(self, id, name, price, store_id):
        self.id = id
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name":self.name, "price":self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #alter coommand = return cls.query.filter_by(name=name).first()

    def save_to_db(self): #Here self = Object of item
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self): #Here self = Object of item
        db.session.delete(self)
        db.session.commit()
