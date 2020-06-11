import time
from database_config import Session
from errors import StockNotFoundError, TradeConstraintError
from flask import Blueprint, jsonify, request
from models import User, Trade
from marshmallow import ValidationError
from schemas import UserSchema, BalanceSchema, TradeSchema
from sqlalchemy.orm.exc import NoResultFound
from consumers import stocks

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
            return jsonify(error="user not found"), 404

    @controller.route("/withdraw", methods=["PUT", "PATCH"])
    def withdraw():
        try:
            body = UserController.balance_schema.load(request.get_json())
            user = session.query(User).filter(
                User.user_id == body["user_id"]).one()
            if user.amount < body["amount"]:
                return jsonify(error="insufficient user amount"), 400
            user.amount -= body["amount"]
            session.commit()
            return jsonify(UserController.user_schema.dump(user)), 200
        except ValidationError as err:
            return err.messages, 400
        except NoResultFound as e:
            return jsonify(error="user not found"), 404

    @controller.route("/deposit", methods=["PUT", "PATCH"])
    def deposit():
        try:
            body = UserController.balance_schema.load(request.get_json())
            user = session.query(User).filter(
                User.user_id == body["user_id"]).one()
            user.amount += body["amount"]
            session.commit()
            return jsonify(UserController.user_schema.dump(user)), 200
        except ValidationError as err:
            return err.messages, 400
        except NoResultFound as e:
            return jsonify(error="user not found"), 404


class StockController:

    @controller.route("/stocks/<stock_id>", methods=["GET"])
    def get_stock(stock_id):
        stock = stocks.get(stock_id)
        if stock is None:
            return jsonify(error="stock not found"), 404
        return jsonify(stock), 200


class TradeController:
    trade_schema = TradeSchema()
    user_schema = UserSchema()

    @controller.route("/buy", methods=["POST"])
    def buy():
        """
        in order for the user to be able to buy stock the following must be satisified:
        - user exists
        - stock exists
        - stock price is between upper and lower bound
        - the user has an amount equal to or greater than the total price
        - the number of stock available is greater than or equal to the total number of stock a user want to buy
        once all of the above is satisified the user amount is decremented and a new trade record is created to represent a buy 
        """
        try:
            body, user, stock = TradeController._validate_trade_constraints(
                request)
            if stock["availability"] < body["total"]:
                return jsonify(error="insufficient number of stocks. Number of available stock is {}".format(stock["availability"])), 400
            trade_price = int(stock["price"] * body["total"])
            if user.amount < trade_price:
                return jsonify(error="insufficient user amount. Required amount {} while user amount is {}".format(trade_price, user.amount)), 400
            user.amount -= int(stock["price"] * body["total"])
            body["stock_price"] = stock["price"]
            trade = Trade(**body)
            session.add(trade)
            session.commit()
            return jsonify(TradeController.trade_schema.dump(trade)), 201
        except ValidationError as err:
            return err.messages, 400
        except NoResultFound:
            return jsonify(error="user not found"), 404
        except StockNotFoundError as err:
            return jsonify(error=err.message), 404
        except TradeConstraintError as err:
            return jsonify(error=err.message), 400

    @controller.route("/sell", methods=["POST"])
    def sell():
        """
        in order for the user to be able to sell stock the following must be satisified:
        - user exists
        - stock exists
        - stock price is between upper and lower bound
        - the user holds stocks equal to or greater than the number of stocks he wants to sell
        once all of the above is satisified the user amount is incremented and a new trade record is created with a negative total to represent a sell 
        """
        try:
            body, user, stock = TradeController._validate_trade_constraints(
                request)
            trades = TradeController.user_schema.dump(user)["trades"]
            user_holding_stocks = [
                trade for trade in trades if trade['stock_id'] == stock['stock_id']]
            stock_total = sum(trade["total"] for trade in user_holding_stocks)
            if stock_total < body["total"]:
                return jsonify(error="insufficient number of stocks. User owns {} stocks of stock {}".format(stock_total, stock["name"])), 400
            user.amount += int(stock["price"] * body["total"])
            body["stock_price"] = stock["price"]
            body["total"] *= -1
            trade = Trade(**body)
            session.add(trade)
            session.commit()
            return jsonify(TradeController.trade_schema.dump(trade)), 201
        except ValidationError as err:
            return err.messages, 400
        except NoResultFound:
            return jsonify(error="user not found"), 404
        except StockNotFoundError as err:
            return jsonify(error=err.message), 404
        except TradeConstraintError as err:
            return jsonify(error=err.message), 400

    def _validate_trade_constraints(request):
        body = TradeController.trade_schema.load(request.get_json())
        user = session.query(User).filter(
            User.user_id == body["user_id"]).one()
        stock = stocks.get(body["stock_id"])
        if stock is None:
            raise StockNotFoundError()
        if stock["price"] > body["upper_bound"] or stock["price"] < body["lower_bound"]:
            raise TradeConstraintError(
                "current stock price {} is not within set bounds".format(stock["price"]))
        return body, user, stock
