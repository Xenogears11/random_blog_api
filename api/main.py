import tornado.ioloop
import tornado.web
from handlers import posts, categories, users, blog
from tornado.log import enable_pretty_logging

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(help_page)

#router
def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/posts', posts.PostsHandler),
        (r'/posts/(\d+)', posts.PostsHandler),
        (r'/posts/(\d+)/restore', posts.PostsRestoreHandler),
        (r'/posts/(\d+)/author', posts.PostsAuthorHandler),
        (r'/categories', categories.CategoriesHandler),
        (r'/categories/(\d+)', categories.CategoriesHandler),
        (r'/blog/home', blog.HomeHandler),
        (r'/blog/category/(\d+)', blog.CategoryHandler),
<<<<<<< HEAD
        (r'/blog/edit_post/(\d+)', blog.PostEditHandler)
    ], debug = False)
=======
        (r'/blog/edit_post/(\d+)', blog.PostEditHandler),
        (r'/users', users.UsersHandler),
        (r'/users/(\d+)', users.UsersHandler),
        (r'/auth', blog.AuthHandler),
    ], debug = True)
>>>>>>> refs/heads/dev


#run app
if __name__ == "__main__":
    with open('res/help.txt', 'r', encoding = 'utf-8') as file:
        help_page = file.read()
    enable_pretty_logging()
    app = make_app()
    app.listen(8888)
    print('Ready')
    tornado.ioloop.IOLoop.current().start()
