import tornado.ioloop
import tornado.web
from handlers import posts, categories, all, blog

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(help_page)

def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/posts', posts.PostsHandler),
        (r'/posts/(\d+)', posts.PostsHandler),
        (r'/posts/(\d+)/restore', posts.PostsRestore),
        (r'/categories', categories.CategoriesHandler),
        (r'/categories/(\d+)', categories.CategoriesHandler),
        (r'/all', all.AllHandler),
        (r'/all/(\d+)', all.AllHandler),
        (r'/blog/home', blog.HomeHandler),
        (r'/blog/category/(\d+)', blog.CategoryHandler),
        (r'/blog/edit_post/(\d+)', blog.PostEditHandler)
    ], debug = True)


if __name__ == "__main__":
    with open('res/help.txt', 'r', encoding = 'utf-8') as file:
        help_page = file.read()
    app = make_app()
    app.listen(8888)
    print('Ready')
    tornado.ioloop.IOLoop.current().start()
