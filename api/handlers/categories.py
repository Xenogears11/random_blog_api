from tornado.web import RequestHandler
from database.tables import Posts, Categories
from database.query import QueryPosts, QueryCategories

class CategoriesHandler(RequestHandler):
    def get(self, category_id = None):
        if category_id == None:
            ctgs = QueryCategories.get_all()

            categories = []
            for category in ctgs:
                categories.append(category.toDict())

            self.write({'categories': categories})

        else:
            try:
                category = QueryCategories.get(category_id)
                self.write(category.toDict())
            except:
                self.send_error(404)

    def post(self):
        category = self.get_argument('category')
        ctg = Categories(category)
        QueryCategories.add(ctg)
