"""Queries to categories table.

Methods:
add -- add new category
get -- get category by id
get_all -- get list of all categories
get_first_last -- return id of the first and the last posts in the category
"""

from database.database import DBSession
from database.tables import Posts, Categories


def add(category):
    """Add new category"""
    session = DBSession()

    session.add(category)

    session.commit()
    session.close()


def get(id):
    """Return category by id"""
    session = DBSession()

    category = session.query(Categories).get(id)

    session.close()
    return category


def get_all():
    """Return list of all categories"""
    session = DBSession()

    result = session.query(Categories).all()

    session.close()
    return result


def get_first_last(id):
    """Return id of the first and the last post in the category.

    Returns dictionary, keys : first_id, last_id.
    """

    session = DBSession()

    first_id = session.query(Posts).join(Posts.categories). \
        filter(Categories.id == id, Posts.is_deleted == False). \
        order_by(Posts.id).first().id

    last_id = session.query(Posts).join(Posts.categories). \
        filter(Categories.id == id, Posts.is_deleted == False). \
        order_by(Posts.id.desc()).first().id

    session.close()
    return {
        'first_id': first_id,
        'last_id': last_id
    }
