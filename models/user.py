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

    ##############################################################
    ########### Orace DB part ####################################
    ##############################################################
    # @classmethod
    # def find_by_username(cls, username):
    #
    #     connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM users WHERE username=:username"
    #     result = cursor.execute(query, (username,)) #, (username,)
    #     row = result.fetchone()
    #     if row is not None:
    #         user = cls(row[0], row[1], row[2])
    #     else:
    #         user = None
    #
    #     connection.close()
    #     return user
    #
    # @classmethod
    # def find_by_id(cls, _id):
    #
    #     connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
    #     cursor = connection.cursor()
    #
    #     query = "SELECT * FROM users WHERE id=:id"
    #     result = cursor.execute(query, (_id,)) #, (_id,)
    #     row = result.fetchone()
    #     if row is not None:
    #         user = cls(row[0], row[1], row[2])
    #     else:
    #         user = None
    #
    #     connection.close()
    #     return user
