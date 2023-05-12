from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
from flask import flash

class Recipe:
    db_name = 'recipes'
    def __init__( self , data ):
        self.id = data['id'],
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.dateMade = data['dateMade']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (user_id, name, description, instructions, dateMade, under30) VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(dateMade)s, %(under30)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users on recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users on recipes.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        recipes = []
        if results:
            for user in results:
                recipes.append(user)
            return recipes
        return recipes

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, dateMade = %(dateMade)s ,under30 = %(under30)s WHERE recipes.id = %(recipe_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) <2:
            flash('Recipe name should be more than 2 characters!', 'recipeName')
            is_valid= False
        if len(recipe['description']) <2:
            flash('Recipe description should be more than 2 characters!', 'recipeDescription')
            is_valid= False
        if len(recipe['instructions']) <2:
            flash('Recipe instructions should be more than 2 characters!', 'recipeInstructions')
            is_valid= False
        if recipe['under30'] == '':
            flash('Recipe should have a date!', 'recipeDateMade')
            is_valid= False
        if recipe['dateMade'] == '':
            flash('Recipe should have a time limit!', 'recipeUnder30')
            is_valid= False
        return is_valid

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(recipe_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)