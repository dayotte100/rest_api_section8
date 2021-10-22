# from werkzeug.security import safe_str_cmp
import hmac
# from hmac import compare_digest
# from resources.user import User
from models.usermodel import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username) # Defaults to None if user is not found
    # if user and user.password == password:     # may have issues with python 2.x and unicode
    #if user and user.password == password:
    #    return user
    if user and hmac.compare_digest(user.password, password):
        return user.json()

def identity(payload):  # payload comes from the JWT
    user_id = payload['identity']
    user = UserModel.find_by_id(user_id)
    return user.json()
