from marshmallow import Schema, fields, ValidationError

class TradeSchema(Schema):
    trade_id = fields.Int(dump_only=True)
    stock_id = fields.Str(required=True)
    user_id = fields.Int(required=True)
    total = fields.Int(required=True) 
    lower_bound = fields.Int(required=True)
    upper_bound = fields.Int(required=True)
    stock_price = fields.Int(dump_only=True)
    timestamp = fields.DateTime(dump_only=True)

class UserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    trades = fields.List(fields.Nested(TradeSchema(exclude=["user_id"])))
    username = fields.Str(required=True)
    amount = fields.Int(default=0)

class BalanceSchema(Schema):
    amount = fields.Int(required=True)
    user_id = fields.Int(required=True)
