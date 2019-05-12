#import sqlite3
#import cx_Oracle

from db import db

class StoreModel(db.Model):
    __tablename__ = "stores6"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def json(self):
        return {"name":self.name, "items":[item.json() for item in self.items.all()]} #self.items.all() use that bcz we used lazy="dynamic" in line 13

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #alter coommand = return cls.query.filter_by(name=name).first()

    def save_to_db(self): #Here self = Object of item
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self): #Here self = Object of item
        db.session.delete(self)
        db.session.commit()
