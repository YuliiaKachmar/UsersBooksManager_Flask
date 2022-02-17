from flask_restful import Resource, abort
from flask import request

from Schemas.book_schema import books_schema, book_schema
from db import db
from Models.book import Book, token_required


class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return books_schema.dump(books)


class AddBookResource(Resource):
    @token_required
    def post(self):
        name = request.json['name']
        author = request.json['author']
        pages = request.json['pages']

        if not name or not author or not pages:
            abort(400, message='missing argument')

        new_book = Book(name, author, pages)

        db.session.add(new_book)
        db.session.commit()
        return book_schema.dump(new_book)


class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return book_schema.dump(book)

    @token_required
    def patch(self, book_id):
        book = Book.query.get_or_404(book_id)

        if 'name' in request.json:
            book.name = request.json['name']
        if 'author' in request.json:
            book.author = request.json['author']
        if 'pages' in request.json:
            book.pages = request.json['pages']

        db.session.commit()
        return book_schema.dump(book)

    @token_required
    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return '', 204