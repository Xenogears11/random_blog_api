'''Query classes.

Classes:
QueryPosts - queries to posts tables
QueryCategories - queries to categories tables
'''

from sqlalchemy import Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import joinedload
from database.database import DBSession
from database.tables import Posts, Categories, posts_to_categories_table, Users
from datetime import datetime

class QueryPosts():
    '''Queries to posts table.

    Methods:
    add -- add new post
    get_all -- return list of all posts
    get_all_by_category -- return list of all posts by category
    get -- return post by id
    get_custom -- return list of posts by custom rules
    get_custom_by_category -- return list of posts in a category by custom rules
    update -- update post
    delete -- delete post by id
    restore -- restore post by id
    get_first_last_posts -- return id of the first and the last posts
    '''

    def add(post, categories):
        '''Add new post and return it's id.

        Arguments:
        post - Posts object
        categories - list of categories id
        '''

        session = DBSession()

        session.add(post)
        #add categories to the post
        for id in categories:
            category = session.query(Categories).get(id)
            post.categories.append(category)

        id = post.id

        session.commit()
        session.close()
        return id


    def get_all():
        '''Return list of all posts.'''
        session = DBSession()

        posts = session.query(Posts).filter(Posts.is_deleted == False).\
                order_by(Posts.id.desc()).all()

        session.close()
        return posts


    def get_all_by_category(id):
        '''Return list of all posts in the category by it's id.'''
        session = DBSession()

        posts = session.query(Posts).join(Posts.categories).\
               filter(Categories.id == id, Posts.is_deleted == False).\
               order_by(Posts.id.desc()).all()

        session.close()
        return posts


    def get(id):
        '''Return post by it's id.'''
        session = DBSession()

        post = session.query(Posts).filter(Posts.id == id,
               Posts.is_deleted == False).one()

        session.close()
        return post


    def get_custom(quantity, from_id = None, newer = False):
        '''Return list of posts by custom rules.

        Arguments:
        quantity -- quantity of posts
        from_id -- start from this post
        newer --
            if False - returns older posts
            if True - return newer posts
        '''

        session = DBSession()

        #start from last post if no from_id passed
        if from_id == None:
            posts = session.query(Posts).filter(Posts.is_deleted == False).\
            order_by(Posts.id.desc()).\
            limit(int(quantity)).all()

        #start from custom post
        else:

            #get older posts
            if not newer:
                posts = session.query(Posts).filter(Posts.id <= int(from_id), Posts.is_deleted == False).\
                order_by(Posts.id.desc()).\
                limit(int(quantity)).\
                all()

            #get newer posts
            else:
                posts = session.query(Posts).filter(Posts.id >= int(from_id), Posts.is_deleted == False).\
                order_by(Posts.id).\
                limit(int(quantity)).\
                from_self().\
                order_by(Posts.id.desc()).\
                all()

        session.close()
        return posts


    def get_custom_by_category(category_id, quantity, from_id = None, newer = False):
        '''Return list of posts by custom rules in the selected category.

        Arguments:
        category_id -- id of the category
        quantity -- quantity of posts
        from_id -- start from this post
        newer --
            if False - returns older posts
            if True - return newer posts
        '''

        session = DBSession()

        #start from last post if no from_id passed
        if from_id == None:
            posts = session.query(Posts).join(Posts.categories).\
            filter(Categories.id == category_id, Posts.is_deleted == False).\
            order_by(Posts.id.desc()).\
            limit(int(quantity)).all()

        #start from custom post
        else:

            #get older posts
            if not newer:
                posts = session.query(Posts).join(Posts.categories).\
                filter(Categories.id == category_id,
                       Posts.id <= int(from_id),
                       Posts.is_deleted == False).\
                order_by(Posts.id.desc()).\
                limit(int(quantity)).\
                all()

            #get newer posts
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


    def delete(id):
        '''Delete post by id'''
        session = DBSession()

        post = session.query(Posts).filter(Posts.id == id,
               Posts.is_deleted == False).one()

        #actually just set is_deleted flag to True
        post.is_deleted = True
        post.deletion_date = datetime.now().replace(microsecond=0).isoformat(' ')

        session.commit()
        session.close()


    def update(new_post, categories):
        '''Update post.

        Arguments:
        new_post -- Posts object
        categories - list of categories
        '''

        session = DBSession()

        #get data
        post = session.query(Posts).filter(Posts.id == new_post.id,
               Posts.is_deleted == False).one()

        #update data
        if new_post.header != None:
            post.header = new_post.header

        if new_post.content != None:
            post.content = new_post.content

        if categories:
            post.categories.clear()
            for c in categories:
                category = session.query(Categories).get(c)
                post.categories.append(category)

        post.modification_date = datetime.now().replace(microsecond=0).isoformat(' ')

        session.commit()
        session.close()


    def restore(post_id):
        '''Restore deleted post by id'''
        session = DBSession()

        post = session.query(Posts).filter(Posts.id == post_id,
               Posts.is_deleted == True).one()

        post.modification_date = datetime.now().replace(microsecond=0).isoformat(' ')
        post.deletion_date = None
        post.is_deleted = False

        session.commit()
        session.close()


    def get_first_last_posts():
        '''Return id of the first and the last post

        Returns dictionary, keys : first_id, last_id.
        '''

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
    '''Queries to categories table.

    Methods:
    add -- add new category
    get -- get category by id
    get_all -- get list of all categories
    get_first_last_posts -- return id of the first and the last posts in the category
    '''

    def add(category):
        '''Add new category'''
        session = DBSession()

        session.add(category)

        session.commit()
        session.close()

    def get(id):
        '''Return category by id'''
        session = DBSession()

        category = session.query(Categories).get(id)

        session.close()
        return category

    def get_all():
        '''Return list of all categories'''
        session = DBSession()

        result = session.query(Categories).all()

        session.close()
        return result


    def get_first_last_posts(id):
        '''Return id of the first and the last post in the category.

        Returns dictionary, keys : first_id, last_id.
        '''

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

class QueryUsers():
    '''Queries to users table.

    Methods:
    '''

    def add(user):
        '''Add new user'''
        session = DBSession()

        session.add(user)

        session.commit()
        session.close()

    def get(id):
        '''Get user by id'''
        session = DBSession()

        user = session.query(Users).get(id)

        session.close()
        return user

    def validate(username, password):
        '''Validate user.
        If successfull - returns user's id, else - None.
        '''
        session = DBSession()

        user = session.query(Users).filter(Users.username == username).first()

        session.close()

        if user.password != None and user.password == password:
            return user.id
        else:
            return None
