import os
from flask import Flask, jsonify, request
from model import db, User
from flask_cors import CORS
from flask_migrate import Migrate

BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + \
    os.path.join(BASEDIR, "db.db")
Migrate(app, db)
db.init_app(app)
CORS(app)

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = db.session.query(User).all()
        list_users = list()
        for user in users:
            print("user ",user)
            print("user name",user.name)
            print("user email",user.email)
            list_users.append({"name":user.name, "email":user.email})
        print(users)
        return jsonify({"users":list_users})
    except:
         return jsonify({"msg": "ups! error server"}), 500

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.query(User).get(id)
    print(user)
    if user is not None:
        return jsonify(user.serialize()),200
    else:
        return jsonify({"msg": "user not found"}),404

@app.route('/user', methods=['POST'])
def insert_user():
    user = User()
    user.name = request.json.get("name")
    user.email = request.json.get("email")
    print("user.name ", user.name)
    print("user.email ",user.email)
    if user.name is not None and user.email is not None:
        db.session().add(user)
        db.session().commit()
        return jsonify({"msg":"User success full ","user" : user.serialize()}),201
    else:
        return jsonify({"msg": "bad request"}),500

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.query(User).get(id)
    print(user)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "element delete succes"}),200
    else:
        return jsonify({"msg": "user not found"}),404

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.query(User).get(id)
    print(user)
    if user is not None:
        insert_name =  request.json.get("name")
        insert_email = request.json.get("email")
        if insert_name is not None and insert_email is not None:
            user.name =insert_name
            user.email =insert_email
            db.session.commit()
            return jsonify({"msg": "element delete succes"}),200
        else:
            return jsonify({"msg": "bad request"}),500
    else:
        return jsonify({"msg": "user not found"}),404