from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

#association table
posts_to_categories_table = Table('posts_to_categories', Base.metadata,
    Column('posts_id', Integer, ForeignKey('posts.id')),
    Column('category', Integer, ForeignKey('categories.id'))
)

class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key = True)
    header = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    creation_date = Column(DateTime, nullable = False)
    modification_date = Column(DateTime, nullable = True)
    deletion_date = Column(DateTime, nullable = True)
    is_deleted = Column(Boolean, nullable = False)
    author = Column(String, nullable = False)

    categories = relationship('Categories',
                              secondary = posts_to_categories_table,
                              lazy = 'joined'
                             )

    def __init__(self, header = None, content = None, author = None, id = None):
        self.id = id
        self.header = header
        self.content = content
        self.creation_date = datetime.now().replace(microsecond=0).isoformat(' ')
        self.author = author
        self.is_deleted = False

    def toDict(self):
        ctgs = []
        for c in self.categories:
            ctgs.append(c.category)

        return {
            'id' : self.id,
            'header' : self.header,
            'content' : self.content,
            'creation_date' : str(self.creation_date),
            'modification_date' : str(self.modification_date),
            'deletion_date' : str(self.deletion_date),
            'author' : self.author,
            'categories' : ctgs
        }

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key = True)
    category = Column(String, nullable = False)

    posts = relationship('Posts',
                         secondary = posts_to_categories_table,
                         primaryjoin = "Categories.id == posts_to_categories.c.category",
                         secondaryjoin = "and_(posts_to_categories.c.posts_id == Posts.id, "
                                         "Posts.is_deleted == False)"
                         )

    def __init__(self, category = None, id = None):
        self.category = category

    def toDict(self):
        return {
            'id' : self.id,
            'category' : self.category
        }
