from .db import db

# Book Class/Model
class Book(db.Model):
    # Book Class/Model
    class Book(db.Model):
        id=db.Column(db.Integer, primary_key=True)
        name=db.Column(db.String(100))
        author=db.Column(db.String(100))
        genre=db.Column(db.String(100))
        pages=db.Column(db.Integer)
        read=db.Column(db.Boolean)
    def __init__(self, name, author, genre, pages, read):
        self.name = name
        self.author = author
        self.genre = genre
        self.pages = pages
        self.read = read