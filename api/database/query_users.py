"""Queries to users table.

Methods:
"""

from database.database import DBSession
from database.tables import Users


def add(user):
    """Add new user"""
    session = DBSession()

    session.add(user)

    session.commit()
    session.close()


def get(id):
    """Get user by id"""
    session = DBSession()

    user = session.query(Users).get(id)

    session.close()
    return user


def validate(username, password):
    """Validate user.
    If successfull - returns user's id, else - None.
    """
    session = DBSession()

    user = session.query(Users).filter(Users.username == username).first()

    session.close()

    if user is not None and user.password == password:
        return user.id
    else:
        return None
