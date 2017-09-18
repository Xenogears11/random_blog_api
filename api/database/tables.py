'''SQLAlchemy table classes.'''

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

#Association table
posts_to_categories_table = Table('posts_to_categories', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)

class Posts(Base):
    '''Table posts'''
    __tablename__ = 'posts'

    #Columns
    id = Column(Integer, primary_key = True)
    header = Column(String, nullable = False)
    content = Column(Text, nullable = False)
    creation_date = Column(DateTime, nullable = False)
    modification_date = Column(DateTime, nullable = True)
    deletion_date = Column(DateTime, nullable = True)
    is_deleted = Column(Boolean, nullable = False)
    author = Column(String, nullable = False)

    #Relationships
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
        '''Returns object as dictionary'''
        ctgs = []
        for c in self.categories:
            ctgs.append(c.category)

        result = {
            'id' : self.id,
            'header' : self.header,
            'content' : self.content,
            'creation_date' : None,
            'modification_date' : None,
            'deletion_date' : None,
            'author' : self.author,
            'categories' : ctgs
        }

        if self.creation_date != None:
            result['creation_date'] = self.creation_date.strftime('%d %B %Y - %H:%M')

        if self.modification_date != None:
            result['modification_date'] = self.modification_date.strftime('%d %B %Y - %H:%M')

        if self.deletion_date != None:
            result['deletion_date'] = self.deletion_date.strftime('%d %B %Y - %H:%M')

        return result

class Categories(Base):
    '''Table categories'''
    __tablename__ = 'categories'

    #Columns
    id = Column(Integer, primary_key = True)
    category = Column(String, nullable = False)

    #Relationships
    posts = relationship('Posts',
                         secondary = posts_to_categories_table,
                         )

    def __init__(self, category = None, id = None):
        self.category = category

    def toDict(self):
        '''Returns object as dictionary'''
        return {
            'id' : self.id,
            'category' : self.category
        }
