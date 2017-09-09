from tornado.web import RequestHandler
from database.tables import Posts, Categories
from database.query import QueryPosts, QueryCategories

class HomeHandler(RequestHandler):
    def get(self):
        from_id = self.get_argument('from_id', default = None)
        quantity = self.get_argument('quantity', default = None)

        result = {}

        ps = QueryPosts.get_param(from_id, quantity)
        ctgs = QueryCategories.get_all()

        posts = []
        for post in ps:
            posts.append(post.toDict())
        result['posts'] = posts

        categories = []
        for category in ctgs:
            categories.append(category.toDict())
        result['categories'] = categories

        self.write(result)

class CategoryHandler(RequestHandler):
    def get(self, id = None):
        result = {}

        category = QueryCategories.get(id)
        ps = QueryPosts.get_by_category(id)
        ctgs = QueryCategories.get_all()

        result['category'] = category.toDict()

        posts = []
        for post in ps:
            posts.append(post.toDict())
        result['posts'] = posts

        categories = []
        for category in ctgs:
            categories.append(category.toDict())
        result['categories'] = categories

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
