from marshmallow import fields, validates, ValidationError

from ma import ma
from Models.book import Book


class BookSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    author = fields.Str()
    pages = fields.Integer()

    class Meta:
        fields = ("id", "name", "author", "pages")
        model = Book

    @validates("pages")
    def validate_quantity(self, value):
        if value < 1:
            raise ValidationError("Pages must be greater than 1.")


book_schema = BookSchema()
books_schema = BookSchema(many=True)