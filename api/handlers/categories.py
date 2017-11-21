"""Handlers for categories table."""

from tornado.web import RequestHandler
from database.tables import Categories
from database import query_categories


class CategoriesHandler(RequestHandler):
    """Handler for categories table.

    Methods:
    - post
    - get
    """

    def post(self):
        """Add new category

        Request arguments:
        category -- new category name
        """

        category = self.get_argument('category')
        ctg = Categories(category)
        query_categories.add(ctg)

    def get(self, id=None):
        """Return category by id or list of categories(if no id passed)."""

        # return all categories if no id passed
        if id is None:
            ctgs = query_categories.get_all()

            categories = []
            for category in ctgs:
                categories.append(category.to_dict())

            self.write({'categories': categories})

        # return category by id
        else:
            try:
                category = query_categories.get(id)
                self.write(category.to_dict())
            except:
                self.send_error(404)
