from tornado.web import RequestHandler
from database.tables import Posts, Categories
from database.query import QueryPosts, QueryCategories

class PostsHandler(RequestHandler):
    def get(self, post_id = None):
        if post_id == None:
            category_id = self.get_argument('category_id', default = None)

            if category_id == None:
                result = QueryPosts.get_all()
            else:
                try:
                    result = QueryPosts.get_by_category(int(category_id))
                except:
                    self.send_error(404)

            posts = []
            for post in result:
                posts.append(post.toDict())

            self.write({'posts' : posts})

        else:
            try:
                post = QueryPosts.get(post_id)
                self.write(post.toDict())
            except:
                self.send_error(404)

    def post(self):
        header = self.get_argument('header')
        content = self.get_argument('content')
        author =  self.get_argument('author')
        categories = self.get_arguments('categories')

        if not categories:
            self.send_error(400)
        else:
            post = Posts(header, content, author)
            id = QueryPosts.add(post, categories)
            self.write({'id':id})

    def put(self, post_id = None):
        header = self.get_argument('header', default = None)
        content = self.get_argument('content', default = None)
        author =  self.get_argument('author', default = None)
        categories = self.get_arguments('categories')

        post = Posts(header, content, author, post_id)

        try:
            QueryPosts.update(post, categories)
        except:
            self.send_error(400)

    def delete(self, post_id = None):
        try:
            QueryPosts.delete(post_id)
        except:
            self.send_error(400)

class PostsRestore(RequestHandler):
    def put(self, post_id = None):
        try:
            QueryPosts.restore(post_id)
        except:
            self.send_error(400)

class PostsParamHandler(RequestHandler):
    def get(self):
        quantity = self.get_argument('quantity', default = None)
        from_id = self.get_argument('from_id', default = None)

        try:
            result = QueryPosts.get_param(from_id, quantity)
        except:
            self.send_error(404)

        posts = []
        for post in result:
            posts.append(post.toDict())

        self.write({'posts' : posts})
