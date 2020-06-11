from database_config import Session
from models import User


def populate():
    session = Session()
    session.add_all({
        User(username="user1", amount=2000),
        User(username="user2", amount=1000),
        User(username="user3", amount=500),
        User(username="user4", amount=800)
    })
    session.commit()
    session.close()


if __name__ == "__main__":
    populate()
