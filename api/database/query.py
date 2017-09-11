from sqlalchemy import Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import joinedload
from database.database import DBSession
from database.tables import Posts, Categories, posts_to_categories_table
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

    def get_all_by_category(id):
        session = DBSession()

        posts = session.query(Posts).join(Posts.categories).\
               filter(Categories.id == id, Posts.is_deleted == False).\
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

    def restore(post_id):
        session = DBSession()

        post = session.query(Posts).filter(Posts.id == post_id,
               Posts.is_deleted == True).one()

        post.modification_date = datetime.now().replace(microsecond=0).isoformat(' ')
        post.deletion_date = None
        post.is_deleted = False

        session.commit()
        session.close()

    def get_custom(quantity, from_id = None, previous = False):
        session = DBSession()

        if from_id == None:
            posts = session.query(Posts).filter(Posts.is_deleted == False).\
            order_by(Posts.id.desc()).\
            limit(quantity).all()

        else:
            if not previous:
                posts = session.query(Posts).filter(Posts.id <= int(from_id), Posts.is_deleted == False).\
                order_by(Posts.id.desc()).\
                limit(int(quantity)).\
                all()
            else:
                posts = session.query(Posts).filter(Posts.id >= int(from_id), Posts.is_deleted == False).\
                order_by(Posts.id).\
                limit(int(quantity)).\
                from_self().\
                order_by(Posts.id.desc()).\
                all()

        session.close()
        return posts

    def get_custom_by_category(category_id, quantity, from_id = None, previous = False):
        session = DBSession()

        if from_id == None:
            posts = session.query(Posts).join(Posts.categories).\
            filter(Categories.id == category_id, Posts.is_deleted == False).\
            order_by(Posts.id.desc()).\
            limit(int(quantity)).all()

        else:
            if not previous:
                posts = session.query(Posts).join(Posts.categories).\
                filter(Categories.id == category_id,
                       Posts.id <= int(from_id),
                       Posts.is_deleted == False).\
                order_by(Posts.id.desc()).\
                limit(int(quantity)).\
                all()
            else:
                posts = session.query(Posts).join(Posts.categories).\
                filter(Categories.id == category_id,
                       Posts.id >= int(from_id),
                       Posts.is_deleted == False).\
                order_by(Posts.id).\
                limit(int(quantity)).\
                from_self().\
                order_by(Posts.id.desc()).\
                all()

        session.close()
        return posts

    def get_first_last_posts():
        session = DBSession()

        first_id = session.query(Posts).filter(Posts.is_deleted == False).\
        order_by(Posts.id).first().id

        last_id = session.query(Posts).filter(Posts.is_deleted == False).\
        order_by(Posts.id.desc()).first().id

        session.close()
        return {
            'first_id' : first_id,
            'last_id' : last_id
        }

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

    def add(category):
        session = DBSession()

        session.add(category)

        session.commit()
        session.close()

    def get_first_last_posts(id):
        session = DBSession()

        first_id = session.query(Posts).join(Posts.categories).\
        filter(Categories.id == id, Posts.is_deleted == False).\
        order_by(Posts.id).first().id

        last_id = session.query(Posts).join(Posts.categories).\
        filter(Categories.id == id, Posts.is_deleted == False).\
        order_by(Posts.id.desc()).first().id

        session.close()
        return {
            'first_id' : first_id,
            'last_id' : last_id
        }
