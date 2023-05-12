from flask_app.config.mysqlconnection import connectToMySQL
import re, datetime
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'recipes'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
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
                users.append(cls(user))
            return users
        return users

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if results:
            return results[0]
        return False

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

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
