'''Custom handlers for Random blog.'''

from tornado.web import RequestHandler
from database.tables import Posts, Categories
from database.query import QueryPosts, QueryCategories

class HomeHandler(RequestHandler):
    '''Home page.'''

    def get(self):
        '''Return data for Home page.

        Request arguments:
        from_id -- start from this post
        quantity -- quantity of posts
        newer --
            if not passed - returns older posts
            if passed any value - return newer posts

        Data:
        - 'posts' : list of posts
        - 'categories' : list of all categories
        - 'first_last_posts' : id of the first and the last posts
        '''

        #get arguments
        from_id = self.get_argument('from_id', default = None)
        quantity = self.get_argument('quantity', default = None)
        newer = self.get_argument('newer', default = None)
        if newer == None:
            newer = False
        else:
            newer = True

        #get data from db
        ps = QueryPosts.get_custom(quantity, from_id, newer)
        ctgs = QueryCategories.get_all()
        first_last_posts = QueryPosts.get_first_last_posts()

        #form response
        response = {}

        posts = []
        for post in ps:
            posts.append(post.toDict())
        response['posts'] = posts

        categories = []
        for category in ctgs:
            categories.append(category.toDict())
        response['categories'] = categories

        response['first_last_posts'] = first_last_posts

        #send response
        self.write(response)

class CategoryHandler(RequestHandler):
    '''Category/<id> page.'''

    def get(self, id = None):
        '''Return data for Category/<id> page.

        Arguments:
        id -- id of the category

        Request arguments:
        from_id -- start from this post
        quantity -- quantity of posts
        newer --
            if not passed - returns older posts
            if passed any value - return newer posts

        Data:
        - 'category' : requested category
        - 'posts' : list of posts in the category
        - 'categories' : list of all categories
        - 'first_last_posts' : id of the first and the last posts in the category
        '''

        #get arguments
        from_id = self.get_argument('from_id', default = None)
        quantity = self.get_argument('quantity', default = None)
        newer = self.get_argument('newer', default = None)
        if newer == None:
            newer = False
        else:
            newer = True

        #get data from db
        category = QueryCategories.get(id)
        ps = QueryPosts.get_custom_by_category(id, quantity, from_id, newer)
        ctgs = QueryCategories.get_all()
        first_last_posts = QueryCategories.get_first_last_posts(id)

        #form response
        response = {}

        response['category'] = category.toDict()

        posts = []
        for post in ps:
            posts.append(post.toDict())
        response['posts'] = posts

        categories = []
        for category in ctgs:
            categories.append(category.toDict())
        response['categories'] = categories

        response['first_last_posts'] = first_last_posts

        #send response
        self.write(response)

class PostEditHandler(RequestHandler):
    '''Edit post page.'''

    def get(self, id = None):
        '''Return data for Edit post page.

        Arguments:
        id -- id of the post

        Data:
        - 'post' : post data
        - 'categories' : list of all categories
        '''

        #get data from db
        post = QueryPosts.get(id)
        ctgs = QueryCategories.get_all()

        #form response
        response = {}

        response['post'] = post.toDict()

        categories = []
        for category in ctgs:
            categories.append(category.toDict())
        response['categories'] = categories

        #send response
        self.write(response)
