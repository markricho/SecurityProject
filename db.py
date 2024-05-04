'''
db
database file, containing all the logic to interface with the sql database
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *

from pathlib import Path

# creates the database directory
Path("database") \
    .mkdir(exist_ok=True)

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display the sql output
engine = create_engine("sqlite:///database/main.db", echo=False)

# initializes the database
Base.metadata.create_all(engine)

# inserts a user to the database
def insert_user(username: str, password: str):
    with Session(engine) as session:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()

# gets a user from the database
def get_user(username: str):
    with Session(engine) as session:
        return session.get(User, username)

# try and add a friend to the database for current user
def add_friend(user_username: str, friend_username: str):
    with Session(engine) as session:
        friend = session.query(User).filter(User.username == friend_username).first()

        if friend:
            user = session.query(User).filter(User.username == user_username).first()
            if user:
                user.friends.append(friend)
                session.commit()
                print("Friend added successfully.")
            else:
                print("User not found.")
        else:
            print("Friend not found.")

