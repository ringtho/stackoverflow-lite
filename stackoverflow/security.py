from user import User

users = [
    {
        "id":1,
        "username": "sringtho",
        "email": "sringtho@gmail.com",
        "fullname": "Smith Ringtho",
        "sex":"male",
        "password": "abcdef"
    }
    

]

username_mapping = {
    "sringtho": {
        "id":1,
        "username": "sringtho",
        "email": "sringtho@gmail.com",
        "fullname": "Smith Ringtho",
        "sex":"male",
        "password": "abcdef"
    }
    # u.username : u for u in users
    }
userid_mapping = {
        1 : {
        "id":1,
        "username": "sringtho",
        "email": "sringtho@gmail.com",
        "fullname": "Smith Ringtho",
        "sex":"male",
        "password": "abcdef"
    }
    # u.id : u for u in users
    }

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

User(1,'sringtho','sringtho@gmail.com','Smith Ringtho','male','abcdef')