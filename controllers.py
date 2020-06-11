from database_config import Session
from flask import Blueprint, jsonify, request
import logging
from models import User, Trade
from marshmallow import ValidationError
from schemas import UserSchema, BalanceSchema
from sqlalchemy.orm.exc import NoResultFound
from consumers import stocks

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
controller = Blueprint('controller', __name__)
session = Session()

class UserController:
    user_schema = UserSchema()
    balance_schema = BalanceSchema()

    @controller.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        try:
            user = session.query(User).filter(User.user_id == user_id).one()
            return jsonify(UserController.user_schema.dump(user)), 200
        except NoResultFound as e:
            return jsonify(error= "user not found"), 404
    
    @controller.route("/withdraw", methods=["PUT", "PATCH"])
    def withdraw():
        try:
            body = UserController.balance_schema.load(request.get_json())
            user = session.query(User).filter(User.user_id == body["user_id"]).one()
            if user.amount < body["amount"]:
                return jsonify(error= "insufficient user amount"), 400
            user.amount -= body["amount"]
            session.commit()
            return jsonify(UserController.user_schema.dump(user)), 200
        except ValidationError as err:
                return err.messages, 400 
        except NoResultFound as e:
            return jsonify(error= "user not found"), 404

    @controller.route("/deposit", methods=["PUT", "PATCH"])
    def deposit():
        try:
            body = UserController.balance_schema.load(request.get_json())
            user = session.query(User).filter(User.user_id == body["user_id"]).one()
            user.amount += body["amount"]
            session.commit()
            return jsonify(UserController.user_schema.dump(user)), 200
        except ValidationError as err:
                return err.messages, 400 
        except NoResultFound as e:
            return jsonify(error= "user not found"), 404

class StockController:

    @controller.route("/stocks/<stock_id>", methods=["GET"])
    def get_stock(stock_id):
        stock = stocks.get(stock_id)
        if stock is None:
            return jsonify(error= "stock not found"), 404
        return jsonify(stock), 200
