import sqlite3
import cx_Oracle

from db import db

#####################################################
##### Finding User Class ############################
#####################################################
class UserModel(db.Model):
    __tablename__ = "users6"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, id, username, password): #id,
        self.id = id #db.engine.execute('SELECT (NVL(MAX(ID),0)+1) FROM users6')
        self.username = username
        self.password = password

    def save_to_db(self): #Here self = Object of item
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
