import tornado.ioloop
import tornado.web
from handlers.posts import PostsHandler, PostsRestore
from handlers.categories import CategoriesHandler
from handlers.all import AllHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(help_page)

def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/posts', PostsHandler),
        (r'/posts/(\d+)', PostsHandler),
        (r'/posts/(\d+)/restore', PostsRestore),
        (r'/categories', CategoriesHandler),
        (r'/categories/(\d+)', CategoriesHandler),
        (r'/all', AllHandler),
        (r'/all/(\d+)', AllHandler)
    ], debug = True)


if __name__ == "__main__":
    with open('res/help.txt', 'r', encoding = 'utf-8') as file:
        help_page = file.read()
    app = make_app()
    app.listen(8888)
    print('Ready')
    tornado.ioloop.IOLoop.current().start()
