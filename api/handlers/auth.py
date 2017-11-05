'''Auth handlers.'''

from tornado.web import RequestHandler
from database.tables import Users
from database.query import QueryUsers

class AuthHandler(RequestHandler):
    '''Auth handler.'''

    def post(self):
        #get arguments
        username = self.get_argument('username')
        password = self.get_argument('password')

        id = QueryUsers.validate(username, password)

        response = {}

        if id != None:
            response = {
                'validated' : True,
                'user_id' : id
            }

        else:
            response['validated'] = False

        try:
            self.write(response)
        except:
            abort(404)
