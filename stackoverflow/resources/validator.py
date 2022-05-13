import re

class QuestionValidator:
    def __init__(self, request):
        self.request = request

    def question_is_valid(self):
        try:
            question = self.request.get_json()
            assert isinstance(question, dict),'Ensure that the question is in json format'
            self.ensure_no_empty_fields(question)
            self.ensure_valid_data_types(question)
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def ensure_no_empty_fields(self, question):
        assert 'title' in question, "'title' field not specified as the dictionary key"
        assert 'description' in question, "'description' field not specified as the dictionary key"
        assert 'stack' in question, "'stack' field not specified as the dictionary key"

    def ensure_valid_data_types(self, question):
        assert isinstance(question["title"], str), ("Title must be of string type")
        assert isinstance(question["description"], str), ("Description must be of string type")
        assert isinstance(question['stack'], str), ("Stack must be of string type")
     
class UserValidator:
    def __init__(self, request):
        self.request = request

    def validate_user_data(self):
        try:
            user = self.request.get_json()
            assert isinstance(user, dict),'Ensure to enter registration details in json format'
            self.ensure_no_empty_fields(user)
            self.ensure_valid_datatypes(user)
            self.validate_email_address(user["email"])
            self.validate_password(user["password"])
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def ensure_no_empty_fields(self, user):
        assert 'lastname' in user, "'lastname' key not specified in the json data"
        assert 'firstname' in user, "'firstname' key not specified in the json data"
        assert 'email' in user, "'email' key not specified in the json data"
        assert 'gender' in user, "'gender' key not specified in the json data"
        assert 'username' in user, "'username' key not specified in the json data"
        assert 'password' in user, "'password' key not specified in the json data"

    def ensure_valid_datatypes(self, user):
        assert isinstance(user["username"], str), 'Username should be a string'
        assert isinstance(user["firstname"], str), 'Firstname should be a string'
        assert isinstance(user["lastname"], str), 'Lastname should be string'
        assert isinstance(user["gender"], str), 'Lastname should be string'
        assert isinstance(user["password"], str), 'Password should be a string'

    def validate_email_address(self, email):
        assert isinstance(email, str), 'Email address must be a string!'
        pattern = re.compile(r'[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,3}((\.[a-zA-Z]{2,3})+)?$')
        assert pattern.match(email.strip()), 'Invalid Email Address!'

    def validate_password(self, password):
        assert isinstance(password, str), 'Password must be a string!'
        check_password = {
        'a-z': str.islower, 
        'A-Z': str.isupper, 
        '0-9': str.isdigit
        }
        for letter in password:
            for key, value in check_password.items():
                if value(letter):
                    del check_password[key]
                    break 
        password_is_valid = len(check_password) == 0 and 6 <= len(password) <= 64
        error_message = (
            'Password must contain atleast one lowercase letter, one uppercase letter,'
            ' a digit and be 6 to 64 characters long!'
        )
        assert password_is_valid, error_message  

class LoginValidator:
    def __init__(self, request):
        self.request = request

    def validate_login_data(self):
        try:
            user = self.request.get_json()
            self.ensure_no_empty_fields(user)
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def ensure_no_empty_fields(self,user):
        assert 'username' in user, "'username' key not specified in the json data"
        assert 'password' in user, "'password' key not specified in the json data"
        assert isinstance(user, dict),"'Ensure' to enter login details in json format"
    
    # def check_if_user_exists_already(self, username, email):
    #     global cursor
    #     query = """SELECT username FROM users WHERE username='{}'""".format(username)
    #     query1 = """SELECT email FROM users WHERE email='{}'""".format(email)
    #     cursor.execute(query)

    #     if cursor.fetchall():
    #         raise Exception(f'{username} already exists')
        
    #     cursor.execute(query1)
    #     if cursor.fetchall():    
    #         raise Exception(f'{email} already in the system')