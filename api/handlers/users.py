"""Handlers for categories table."""

from tornado.web import RequestHandler
from database.tables import Users
from database import query_users


class UsersHandler(RequestHandler):
    """Handler for users table.

    Methods:
    - post
    - get
    """

    def post(self):
        """Add new user.

        Request arguments:
        username
        password
        """

        # get arguments
        username = self.get_argument('username')
        password = self.get_argument('password')

        try:
            # add user
            user = Users(username=username, password=password)
            query_users.add(user)
        except:
            self.send_error(404)

    def get(self, id=None):
        """Get user.

        Arguments:
        id
        """

        try:
            user = query_users.get(id)
            self.write(user.to_dict())
        except:
            self.send_error(404)
