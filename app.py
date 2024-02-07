from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init App
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


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

# Book Shcema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'author', 'genre', 'pages', 'read')

# Init schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Create a Book
@app.route('/book', methods=['POST'])
def add_book():
    name = request.json['name']
    author = request.json['author']
    genre = request.json['genre']
    pages = request.json['pages']
    read = request.json['read']

    new_book = Book(name, author, genre, pages, read)

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)

# Get All Books
@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)

# Get Single Book
@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)

# Update a Book
@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    name = request.json['name']
    author = request.json['author']
    genre = request.json['genre']
    pages = request.json['pages']
    read = request.json['read']

    book.name = name
    book.author = author
    book.genre = genre
    book.pages = pages
    book.read = read

    db.session.commit()

    return book_schema.jsonify(book)

# Delete Book
@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)
