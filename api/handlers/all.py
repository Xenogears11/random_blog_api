from tornado.web import RequestHandler
from database.tables import Posts, Categories
from database.query import QueryPosts, QueryCategories

class AllHandler(RequestHandler):
    def get(self, category_id = None):
        result = {}

        if category_id == None:
            ps = QueryPosts.get_all()
        else:
            category = QueryCategories.get(category_id)
            ps = QueryPosts.get_by_category(category_id)
            result['category'] = category.toDict()

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
