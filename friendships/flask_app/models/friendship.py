from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Friendship:
    db_name = 'friendships'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query= "INSERT INTO friendships (user_id, friend_id) VALUES (%(user_id)s, %(friend_id)s);"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM friendships"
        results = connectToMySQL(cls.db_name).query_db(query)
        friendships = []
        for result in results:
            friendship = cls(result)
            friendships.append(friendship)
        return friendships

    @classmethod
    def get_by_users(cls, user_id, friend_id):
        query = "SELECT * FROM friendships WHERE (user_id=%(user_id)s AND friend_id=%(friend_id)s) OR (user_id=%(friend_id)s AND friend_id=%(user_id)s);"
        data = {'user_id': user_id, 'friend_id': friend_id}
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM friendships WHERE id=%(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return cls(result[0])
        return result

    @classmethod
    def delete(self,data):
        query = "DELETE FROM friendships WHERE id=%(id)s;"
        connectToMySQL(self.db_name).query_db(query, data)


    @property
    def user(self):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = { 'id': self.user_id }
        result = connectToMySQL(self.db_name).query_db(query, data)
        return result[0]

    @property
    def friend(self):
        query = "SELECT * FROM users WHERE id = %(id)s"
        data = { 'id': self.friend_id }
        result = connectToMySQL(self.db_name).query_db(query, data)
        return result[0]