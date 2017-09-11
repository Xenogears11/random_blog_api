'''Handlers for categories table.'''

from tornado.web import RequestHandler
from database.tables import Posts, Categories
from database.query import QueryPosts, QueryCategories

class CategoriesHandler(RequestHandler):
    '''Handler for categories table.

    Methods:
    - post
    - get
    '''

    def post(self):
        '''Add new category

        Request arguments:
        category -- new category name
        '''

        category = self.get_argument('category')
        ctg = Categories(category)
        QueryCategories.add(ctg)


    def get(self, id = None):
        '''Return category by id or list of categories(if no id passed).'''

        #return all categories if no id passed
        if id == None:
            ctgs = QueryCategories.get_all()

            categories = []
            for category in ctgs:
                categories.append(category.toDict())

            self.write({'categories': categories})

        #return category by id
        else:
            try:
                category = QueryCategories.get(id)
                self.write(category.toDict())
            except:
                self.send_error(404)
