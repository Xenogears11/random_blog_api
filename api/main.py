import tornado.ioloop
import tornado.web
from handlers import posts, categories, blog

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
        #(r'/posts/custom', posts.PostsCustomHandler),
        (r'/categories', categories.CategoriesHandler),
        (r'/categories/(\d+)', categories.CategoriesHandler),
        (r'/blog/home', blog.HomeHandler),
        (r'/blog/category/(\d+)', blog.CategoryHandler),
        (r'/blog/edit_post/(\d+)', blog.PostEditHandler)
    ], debug = True)


#run app
if __name__ == "__main__":
    with open('res/help.txt', 'r', encoding = 'utf-8') as file:
        help_page = file.read()
    app = make_app()
    app.listen(8888)
    print('Ready')
    tornado.ioloop.IOLoop.current().start()
