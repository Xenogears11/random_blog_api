'''Handlers for categories table.'''

from tornado.web import RequestHandler
from database.tables import Users, Posts, Categories
from database.query import QueryPosts, QueryCategories, QueryUsers

class UsersHandler(RequestHandler):
    '''Handler for users table.

    Methods:
    - post
    - get
    '''

    def post(self):
        '''Add new user.

        Request arguments:
        username
        password
        '''

        #get arguments
        username = self.get_argument('username')
        password = self.get_argument('password')

        try:
            #add user
            user = Users(username = username, password = password)
            QueryUsers.add(user)
        except:
            self.send_error(404)

    def get(self, id = None):
        '''Get user.

        Arguments:
        id
        '''

        try:
            user = QueryUsers.get(id)
            self.write(user.toDict())
        except:
            self.send_error(404)
