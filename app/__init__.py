from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS
from .models import Book, db

def create_app(database_uri="sqlite:///db.sqlite3"):
    # Init App
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    ma = Marshmallow(app) 

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
        book = db.session.get(Book, id)
        print(book)
        if book is None:
            return jsonify({'message': 'Book not found'}), 404
        return book_schema.jsonify(book)

    # Update a Book
    @app.route('/book/<id>', methods=['PUT'])
    def update_book(id):
        book = db.session.get(Book, id)

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
        book = db.session.get(Book, id)
        db.session.delete(book)
        db.session.commit()

        return jsonify({'message': 'Book deleted'})

    return app

# Run Server
if __name__ == '__main__':
    app = create_app()
    app.run(port=8000, debug=True, host='0.0.0.0')

