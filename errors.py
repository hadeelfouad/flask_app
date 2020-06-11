class StockNotFoundError(Exception):
    def __init__(self, message="stock not found"):
        self.message = message
        super().__init__(message)


class TradeConstraintError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
