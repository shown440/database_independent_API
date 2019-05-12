#import sqlite3
#import cx_Oracle

from flask_restful import Resource, reqparse

from models.user import UserModel
from db import db

###############################################################
###### User Register/ Signup Class ############################
###############################################################
class UserRegister(Resource):
    ##############################################################
    ########### Signin to SQLite3 DB part ########################
    ##############################################################
    parser = reqparse.RequestParser()

    # parser.add_argument("id",
    #     type = int,
    #     required = True,
    #     help = "ID cannot be blank."
    # )
    parser.add_argument("username",
        type = str,
        required = True,
        help = "User name cannot be blank."
    )
    parser.add_argument("password",
        type = str,
        required = True,
        help = "Password name cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message":"{} is already exist".format(data["username"])}, 400

        sql = db.text('SELECT (NVL(MAX(ID),0)+1) FROM users6')
        user_master_id = db.engine.execute(sql).fetchone()
        #print("Type of id = ", type(user_master_id[0]))
        #print("***###",user_master_id[0])

        user = UserModel(user_master_id[0], data["username"], data["password"]) # UserModel(data["id"], data["username"], data["password"]) = UserModel(**data)
        user.save_to_db()

        return {"message":"{} is created successfully as your authentication user".format(data["username"])}, 201

    ##############################################################
    ########### Signin to Oracle DB part ########################
    ##############################################################
    # parser = reqparse.RequestParser()
    #
    # parser.add_argument("username",
    #     type = str,
    #     required = True,
    #     help = "User name cannot be blank."
    # )
    # parser.add_argument("password",
    #     type = str,
    #     required = True,
    #     help = "Password name cannot be blank."
    # )
    # parser.add_argument("role",
    #     type = str,
    #     required = True,
    #     help = "Role name cannot be blank."
    # )
    #
    # def post(self):
    #     data = UserRegister.parser.parse_args()
    #
    #     if User.find_by_username(data["username"]):
    #         return {"message":"{} is already exist".format(data["username"])}, 400
    #
    #     connection = cx_Oracle.connect("shifullah/shifullah@10.11.201.251:1521/stlbas")
    #     cursor = connection.cursor()
    #
    #     # int=INTEGER. but if we need auto incremented id then we have to write INTEGER
    #     insert_query = "INSERT INTO users VALUES(:1, :2, :3, :4)"
    #     cursor.execute(insert_query, (None, data["username"], data["password"], data["role"]))
    #
    #     connection.commit()
    #     connection.close()
    #
    #     return {"message":"{} is created successfully as your authentication user".format(data["username"])}, 201
