'''Handlers for posts table.

Handlers:
PostsHandler -- CRUD operations
PostsRestoreHandler -- restore posts
PostsCustomHandler -- handler for custom requests
'''

from tornado.web import RequestHandler
from database.tables import Posts, Categories
from database.query import QueryPosts, QueryCategories

class PostsHandler(RequestHandler):
    '''CRUD operations for posts table.

    Methods:
    - post
    - get
    - put
    - delete
    '''

    def post(self):
        '''Add new post and return it's id.

        Request agruments:
        header -- post header
        content -- post content
        author -- author of the post
        categories -- list of categories
        '''

        #get arguments
        header = self.get_argument('header')
        content = self.get_argument('content')
        author_id = self.get_argument('author_id')
        categories = self.get_arguments('categories')

        #add new post
        if not categories:
            self.send_error(400)
        else:
            post = Posts(header = header, content = content, author_id = author_id)
            id = QueryPosts.add(post, categories)
            self.write({'id':id})


    def get(self, post_id = None):
        '''Get post by id, list of all posts, or list of all posts by category.

        Arguments:
        id -- id of the post

        Request arguments:
        category_id -- id of the category
        '''

        #get list of posts if no id passed
        if post_id == None:
            category_id = self.get_argument('category_id', default = None)

            #get all posts if no category passed
            if category_id == None:
                result = QueryPosts.get_all()

            #get all posts by category
            else:
                try:
                    result = QueryPosts.get_all_by_category(int(category_id))
                except:
                    self.send_error(404)

            #form response
            posts = []
            for post in result:
                posts.append(post.toDict())

            self.write({'posts' : posts})

        #get post by id
        else:
            try:
                post = QueryPosts.get(post_id)
                self.write(post.toDict())
            except:
                self.send_error(404)


    def put(self, post_id = None):
        '''Update post.

        Arguments:
        id -- id of the post

        Request agruments:
        header -- post header
        content -- post content
        author -- author of the post
        categories -- list of categories
        '''

        #get arguments
        header = self.get_argument('header', default = None)
        content = self.get_argument('content', default = None)
        categories = self.get_arguments('categories')
        print(post_id)

        #create new post object
        post = Posts(header = header, content = content,id = post_id)

        #update post
        try:
            QueryPosts.update(post, categories)
        except:
            self.send_error(400)


    def delete(self, post_id = None):
        '''Delete post by id.'''
        try:
            QueryPosts.delete(post_id)
        except:
            self.send_error(400)

class PostsRestoreHandler(RequestHandler):
    '''Restore option for posts table.

    Methods:
    - put
    '''

    def put(self, id = None):
        '''Restore a post by id.'''
        try:
            QueryPosts.restore(id)
        except:
            self.send_error(400)

class PostsAuthorHandler(RequestHandler):
    '''Return author id by post's id.'''

    def get(self, id = None):
        '''Return author id'''
        try:
            author_id = QueryPosts.get_author(id)
            self.write({'author_id' : author_id})
        except:
            self.send_error(400)
