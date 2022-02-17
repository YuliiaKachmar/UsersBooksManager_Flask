import jwt
import datetime


class JWToken:

    def __init__(self, bearer_header):
        self.token = self.__get__jwt_token(auth_header=bearer_header)

    @staticmethod
    def __get__jwt_token(auth_header):
        schema, jwt_token = None, None
        if 'Authorization' in auth_header:
            schema, jwt_token = auth_header["Authorization"].split(" ")
        if not schema or not jwt_token:
            raise Exception("Header is invalid!")
        else:
            if not schema == "Bearer":
                raise Exception("Schema is invalid!")

        return jwt_token

    def decode_token(self, string_key):
        return jwt.decode(self.token, string_key, algorithms=['HS256'])

    @staticmethod
    def encode_token(user, string_key):
        return jwt.encode(
            {'id': user.id,
             'is_admin': user.is_admin,
             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            string_key)
