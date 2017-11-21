"""Custom handlers for Random blog."""

from tornado.web import RequestHandler
from database import query_posts, query_categories, query_users


class HomeHandler(RequestHandler):
    """Home page."""

    def get(self):
        """Return data for Home page.

        Request arguments:
        from_id -- start from this post
        quantity -- quantity of posts
        newer --
            if not passed - returns older posts
            if passed any value - return newer posts

        Data:
        - 'posts' : list of posts
        - 'categories' : list of all categories
        - 'first_last_posts' : id of the first and the last posts
        """

        # get arguments
        from_id = self.get_argument('from_id', default=None)
        quantity = self.get_argument('quantity', default=None)
        newer = self.get_argument('newer', default=None)
        if newer is None:
            newer = False
        else:
            newer = True

        # get data from db
        ps = query_posts.get_custom(quantity, from_id, newer)
        ctgs = query_categories.get_all()
        first_last_posts = query_posts.get_first_last()

        # form response
        response = {}

        posts = []
        for post in ps:
            posts.append(post.to_dict())
        response['posts'] = posts

        categories = []
        for category in ctgs:
            categories.append(category.to_dict())
        response['categories'] = categories

        response['first_last_posts'] = first_last_posts

        # send response
        self.write(response)


class CategoryHandler(RequestHandler):
    """Category/<id> page."""

    def get(self, id=None):
        """Return data for Category/<id> page.

        Arguments:
        id -- id of the category

        Request arguments:
        from_id -- start from this post
        quantity -- quantity of posts
        newer --
            if not passed - returns older posts
            if passed any value - return newer posts

        Data:
        - 'category' : requested category
        - 'posts' : list of posts in the category
        - 'categories' : list of all categories
        - 'first_last_posts' : id of the first and the last posts in the category
        """

        # get arguments
        from_id = self.get_argument('from_id', default=None)
        quantity = self.get_argument('quantity', default=None)
        newer = self.get_argument('newer', default=None)
        if newer is None:
            newer = False
        else:
            newer = True

        # get data from db
        category = query_categories.get(id)
        ps = query_posts.get_custom_by_category(id, quantity, from_id, newer)
        ctgs = query_categories.get_all()
        first_last_posts = query_categories.get_first_last(id)

        # form response
        response = {'category': category.to_dict()}

        posts = []
        for post in ps:
            posts.append(post.to_dict())
        response['posts'] = posts

        categories = []
        for category in ctgs:
            categories.append(category.to_dict())
        response['categories'] = categories

        response['first_last_posts'] = first_last_posts

        # send response
        self.write(response)


class PostEditHandler(RequestHandler):
    """Edit post page."""

    def get(self, id=None):
        """Return data for Edit post page.

        Arguments:
        id -- id of the post

        Data:
        - 'post' : post data
        - 'categories' : list of all categories
        """

        # get data from db
        post = query_posts.get(id)
        ctgs = query_categories.get_all()

        # form response
        response = {'post': post.to_dict()}

        categories = []
        for category in ctgs:
            categories.append(category.to_dict())
        response['categories'] = categories

        # send response
        self.write(response)


class AuthHandler(RequestHandler):
    """Auth handler."""

    def post(self):
        # get arguments
        username = self.get_argument('username')
        password = self.get_argument('password')

        id = query_users.validate(username, password)

        response = {}

        if id is not None:
            response = {
                'validated': True,
                'user_id': id
            }

        else:
            response['validated'] = False

        try:
            self.write(response)
        except:
            self.send_error(404)
