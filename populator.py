from database_config import Session
from models import *


def populate():
    session = Session()
    session.add_all({
        User(username="user1", amount=2000),
        User(username="user2", amount=1000),
        User(username="user3", amount=500),
        User(username="user4", amount=800),
        Trade(user_id=1, stock_id="6ffb8e62-92c1-40c7-9d38-5b976a346b62", total=50, stock_price=20,lower_bound=20, upper_bound=50)
    })
    session.commit()

if __name__ == "__main__":
    populate()
