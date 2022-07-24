#import modules
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


#create Flask app
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///libraryDatabase.db"
db = SQLAlchemy(app)

class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    year_of_release = db.Column(db.Integer, nullable=False)


book_put_args = reqparse.RequestParser()
book_put_args.add_argument("author", type=str, help="Please input the Author's name", required=True)
book_put_args.add_argument("title", type=str, help="Please input the Title", required=True)
book_put_args.add_argument("year_of_release", type=int, help="Please input the Release date", required=True)

book_update_args = reqparse.RequestParser()
book_update_args.add_argument("author", type=str)
book_update_args.add_argument("title", type=str)
book_update_args.add_argument("year_of_release", type=int)


resource_fields = {
    'id': fields.Integer,
    'author': fields.String,
    'title': fields.String,
    'year_of_release': fields.Integer
}

class Book(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="Could not find a book with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, book_id):
        args = book_put_args.parse_args()
        result = BookModel.query.filter_by(id=book_id).first()
        if result:
            abort(409, message="Book already exists")
        book = BookModel(id=book_id, author=args['author'], title=args['title'], year_of_release=args['year_of_release'])
        db.session.add(book)
        db.session.commit()
        return book, 201

    @marshal_with(resource_fields)
    def patch(self, book_id):
        args = book_update_args.parse_args()
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="Book doesn't exist in Database")
        
        if args['author']:
            result.author = args['author']
        if args['title']:
            result.title = args['title']
        if args['year_of_release']:
            result.year_of_release = args['year_of_release']
        
        db.sesion.commit()

        return result

    def delete(self, book_id):
        args = book_put_args.parse_args()
        del args[book_id]
        return '', 204

api.add_resource(Book, "/book/<int:book_id>")

if __name__ == "__main__":
    app.run(debug=True)