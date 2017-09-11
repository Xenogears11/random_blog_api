from tornado.web import RequestHandler
from database.tables import Posts, Categories
from database.query import QueryPosts, QueryCategories

class HomeHandler(RequestHandler):
    def get(self):
        from_id = self.get_argument('from_id', default = None)
        quantity = self.get_argument('quantity', default = None)
        previous = self.get_argument('previous', default = None)
        if previous == None:
            previous = False
        else:
            previous = True

        result = {}

        ps = QueryPosts.get_custom(quantity, from_id, previous)
        ctgs = QueryCategories.get_all()
        first_last_ids = QueryPosts.get_first_last_posts()

        posts = []
        for post in ps:
            posts.append(post.toDict())
        result['posts'] = posts

        categories = []
        for category in ctgs:
            categories.append(category.toDict())
        result['categories'] = categories

        result['first_last_posts'] = first_last_ids

        self.write(result)

class CategoryHandler(RequestHandler):
    def get(self, id = None):
        from_id = self.get_argument('from_id', default = None)
        quantity = self.get_argument('quantity', default = None)
        previous = self.get_argument('previous', default = None)
        if previous == None:
            previous = False
        else:
            previous = True

        result = {}

        category = QueryCategories.get(id)
        ps = QueryPosts.get_custom_by_category(id, quantity, from_id, previous)
        ctgs = QueryCategories.get_all()
        first_last_ids = QueryCategories.get_first_last_posts(id)

        result['category'] = category.toDict()

        posts = []
        for post in ps:
            posts.append(post.toDict())
        result['posts'] = posts

        categories = []
        for category in ctgs:
            categories.append(category.toDict())
        result['categories'] = categories

        result['first_last_posts'] = first_last_ids

        self.write(result)

class PostEditHandler(RequestHandler):
    def get(self, id = None):
        result = {}

        post = QueryPosts.get(id)
        ctgs = QueryCategories.get_all()

        result['post'] = post.toDict()

        categories = []
        for category in ctgs:
            categories.append(category.toDict())
        result['categories'] = categories

        self.write(result)
