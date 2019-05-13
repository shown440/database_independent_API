from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# mysql://username:password@server/db
app.config["SQLALCHEMY_DATABASE_URI"] = 'oracle+cx_oracle://shifullah:shifullah@10.11.201.251:1521/stlbas'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres1234@127.0.0.1:5432/db_independent_api'
#app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# its turn off the flask-sqlalchemy modification tracker but don't turn off SQLAlchemy modification tracker
app.secret_key = "shifullah_ahmed_khan"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores/")

api.add_resource(Item, "/item/<string:name>") ### http://127.0.0.1:5000/student/Shifullah
api.add_resource(ItemList, "/items/")

api.add_resource(UserRegister, "/register/")


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.debug=True
    app.run(host="10.11.200.39")
