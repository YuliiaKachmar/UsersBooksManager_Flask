from flask_restful import Api

from Resources.user_resources import LogInUser, UserListResource, UserResource, UserGoogleLogIn,UserRegistration, blueprint
from Resources.book_resources import BookResource, BookListResource, AddBookResource

api = Api()

api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserListResource, '/users')
api.add_resource(UserRegistration, '/signUp')
api.add_resource(LogInUser, '/loginUser')
api.add_resource(UserGoogleLogIn, '/logInGoogle')

api.add_resource(BookResource, '/books/<int:book_id>')
api.add_resource(BookListResource, '/books')
api.add_resource(AddBookResource, '/add_book')