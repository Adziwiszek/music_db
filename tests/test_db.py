from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

# Create SQLite in-memory database
engine = create_engine('sqlite:///:memory:', echo=False)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define Author class
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', back_populates='author')

# Define Book class
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates='books')

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
session = Session(engine)

# Add authors and books to the database
author1 = Author(name='Lem')
book1 = Book(title='Book 1', author=author1)
book2 = Book(title='Book 2', author=author1)

author2 = Author(name='Author 2')
book3 = Book(title='Book 3', author=author2)

session.add_all([author1, author2])
session.commit()

# Query the database to demonstrate the many-to-one relationship
query_author = session.query(Author).filter_by(name='Lem').first()
print(f'Author: {query_author.name}')
print('Books:')
for book in query_author.books:
    print(f'- {book.title}')

session.close()
