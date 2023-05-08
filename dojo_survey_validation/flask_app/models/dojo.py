from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

VALID_LOCATIONS = ['Washington','New York','Los Angelos','Miami']
VALID_LANGUAGE = ['Python','Java','Mern','C#']

class Dojo:
    db_name = 'dojo_survey_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.language = data['language']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def is_valid( dojo ):
        is_valid = True
        # test whether a field matches the pattern
        if len(dojo['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters.")
        if dojo['location'] not in VALID_LOCATIONS:
            is_valid = False
            flash("Must choose one Dojo Location.")
        if dojo['language'] not in VALID_LANGUAGE:
            is_valid = False
            flash("Must choose a favorite language.")
        if len(dojo['comment']) < 3:
            is_valid = False
            flash("Comments must be at least 3 characters.")
        return is_valid

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of users
        dojos = []
        # Iterate over the db results and create instances of users with cls.
        for d in results:
            dojos.append( cls(d) )
        return dojos

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO dojos (name, location, language, comment, created_at, updated_at) VALUES ( %(name)s , %(location)s , %(language)s , %(comment)s, NOW(), NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_last_dojo(cls):
        query = "SELECT * FROM dojos ORDER BY dojos.id DESC LIMIT 1;"
        results = connectToMySQL(cls.db_name).query_db(query)
        return Dojo(results[0])

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM dojos WHERE dojos.id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE dojos SET name=%(name)s, location=%(location)s, language=%(language)s, comment=%(comment)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM dojos WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)