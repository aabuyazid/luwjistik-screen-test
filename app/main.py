import sys
from sys import maxsize
from flask import Flask, Request, g
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from random import sample, randint
from datetime import datetime
import os, logging

DEBUG = False

auth = HTTPBasicAuth()

# Creating an API using a Flask Application
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_BINDS'] = {
    'db2': 'sqlite:///database2',
    'db3': 'sqlite:///database3'
}
db = SQLAlchemy(app)

class OrderModel(db.Model):
    __bind_key__ = 'db3'
    __tablename__ = 'orders'
    id          = db.Column(db.Integer, primary_key=True)
    weight      = db.Column(db.Integer, nullable=False)
    contact     = db.Column(db.String(255), nullable=False)
    sender_addr = db.Column(db.String(255), nullable=False)
    receiv_addr = db.Column(db.String(255), nullable=False)
    checkpoint  = db.Column(db.String(255), nullable=True)
    timestamp   = db.Column(db.DateTime, nullable=True)
    username    = db.Column(db.String(255), nullable=True)

class User(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255), unique=True)
    password_hash = db.Column('password' , db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

# Users for debugging purposes
users = [
    ('john','smithy123'), ('helloworld','thefirst'),
    ('monty','python'), ('python','monty')
]

if not os.path.isfile('./database.db'):
    db.create_all()
    for u in users:
        username, password = u
        user = User(username = username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()


order_post_args = reqparse.RequestParser()
order_post_args.add_argument('weight', type=int, help='weight of the order', required=True)
order_post_args.add_argument('contact', type=str, help='contact information attributed to the order', required=True)
order_post_args.add_argument('sender_addr', type=str, help='address of the sender', required=True)
order_post_args.add_argument('receiv_addr', type=str, help='address of the receiver', required=True)

order_resource_fields = {
    'id'            : fields.Integer,
    'weight'        : fields.Integer,
    'contact'       : fields.String,
    'sender_addr'   : fields.String,
    'receiv_addr'   : fields.String,
    'checkpoint'    : fields.String,  
    'timestamp'     : fields.DateTime,
    'username'      : fields.String
}

order_checkpoints = [
    'Out for delivery',
    'Processed at warehouse',
    'Order picked up',
    'Delivered'
]

class Order(Resource):

    @auth.login_required
    @marshal_with(order_resource_fields)
    def post(self):
        order_id = randint(0,127)
        args = order_post_args.parse_args()

        while OrderModel.query.filter_by(id=order_id).first():
            order_id = randint(0,127)

        order = OrderModel(id=order_id, weight=args['weight'], contact=args['contact'],
                            sender_addr=args['sender_addr'], receiv_addr=args['receiv_addr'],
                            checkpoint=sample(order_checkpoints,1)[0], username=g.user.username,
                            timestamp=datetime.now())
        db.session.add(order)
        db.session.commit()
        return order, 201

    @auth.login_required
    @marshal_with(order_resource_fields)
    def get(self, order_id):
        result = OrderModel.query.filter_by(id=order_id).first()
        if not result:
            abort(404, message=f'Could not find order with ID {order_id}')

        if result.username != g.user.username:
            abort(401, message=f'User {g.user.username} does not have access to this order')

        return result

api.add_resource(Order, "/order", "/order/<int:order_id>")

if __name__ == "__main__":
    app.run(debug=DEBUG)