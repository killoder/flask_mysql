from flask_app.config.mysqlconnection import connectToMySQL
import re, datetime
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'login_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append(user)
            return users
        return users

    @staticmethod
    def is_valid(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,user)

        if len(user['first_name'])<2:
            flash ('First Name must have at least 2 characters !', 'firstNameRegister')
            is_valid=False
        if len(user['last_name'])<2:
            flash ('Last Name must have at least 2 characters !', 'lastNameRegister')
            is_valid=False
        if len(results) >= 1:
            flash("Email already taken !", 'emailRegister')
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email !")
            is_valid=False
        if not re.match(r"^(?=.*[A-Z])(?=.*\d).{8,}$", user['password']):
            flash('Password should be more then 8 characters and have at least 1 number and 1 uppercase !', 'passwordRegister')
            is_valid= False
        if user['password'] != user['confirm_password']:
            flash('Passwords do not match!', 'confirmPasswordRegister')
            is_valid = False
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', user['birthdate']):
            flash("Invalid Birthdate!", 'birthdateRegister')
            is_valid = False
        else:
            birthdate = datetime.datetime.strptime(user['birthdate'], '%Y-%m-%d').date()
            age = (datetime.date.today() - birthdate) // datetime.timedelta(days=365.25)
            if age < 10:
                flash('You must be at least 10 years old to register!', 'birthdateRegister')
                is_valid = False
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', user['birthdate']):
            flash("You must be at least 10 years old in order to register.", 'birthdateRegister')
            is_valid = False
        if not ('gender' in user and user['gender'] in ['male', 'female', 'other']):
            flash("Please provide your gender !", 'genderRegister')
            is_valid = False
        if not ('interests' in user and isinstance(user['interests'], list) and all(x in ['python', 'java', 'mern'] for x in user['interests'])):
            flash("Please check at least one of your interests !", 'interestsRegister')
            is_valid = False
        return is_valid

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM users WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE users.email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
