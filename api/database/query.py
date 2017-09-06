from sqlalchemy import Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import joinedload
from database.database import DBSession
from database.tables import Posts, Categories
from datetime import datetime

class QueryPosts():
    def add(post, categories):
        session = DBSession()

        session.add(post)
        for id in categories:
            category = session.query(Categories).get(id)
            post.categories.append(category)

        id = post.id

        session.commit()
        session.close()
        return id

    def get_all():
        session = DBSession()

        posts = session.query(Posts).filter(Posts.is_deleted == False).\
                order_by(Posts.id.desc()).all()

        session.close()
        return posts

    def get(id):
        session = DBSession()

        post = session.query(Posts).filter(Posts.id == id,
               Posts.is_deleted == False).one()

        session.close()
        return post

    def delete(id):
        session = DBSession()

        post = session.query(Posts).filter(Posts.id == id,
               Posts.is_deleted == False).one()

        post.is_deleted = True
        post.deletion_date = datetime.now().replace(microsecond=0).isoformat(' ')

        session.commit()
        session.close()

    def update(new_post, categories):
        session = DBSession()

        post = session.query(Posts).filter(Posts.id == new_post.id,
               Posts.is_deleted == False).one()

        if new_post.header != None:
            post.header = new_post.header

        if new_post.content != None:
            post.content = new_post.content

        if new_post.author != None:
            post.author = new_post.author

        if categories:
            post.categories.clear()
            for c in categories:
                category = session.query(Categories).get(c)
                post.categories.append(category)

        post.modification_date = datetime.now().replace(microsecond=0).isoformat(' ')

        session.commit()
        session.close()

class QueryCategories():
    def get(id):
        session = DBSession()

        category = session.query(Categories).get(id)

        session.close()
        return category

    def get_all():
        session = DBSession()

        result = session.query(Categories).all()

        session.close()
        return result

    def get_posts(id):
        session = DBSession()

        category = session.query(Categories).\
                   options(joinedload('posts').joinedload('categories')).\
                   get(id)
        posts = category.posts

        session.close()
        return posts

    def add(category):
        session = DBSession()

        session.add(category)

        session.commit()
        session.close()
