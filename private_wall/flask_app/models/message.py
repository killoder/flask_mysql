from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math
from flask import flash

class Message:
    db_name = 'wall_schema'
    def __init__( self , data ):
        self.id = data['id']
        self.message = data['message']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.receiver_id = data['receiver_id']
        self.receiver = data['receiver']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def save(cls, data):
        query = "INSERT INTO messages (sender_id, receiver_id, message) VALUES (%(sender_id)s, %(receiver_id)s, %(message)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_received_messages(cls, data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id =  %(id)s ORDER BY created_at DESC"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        messages = []
        if results:
            for user in results:
                messages.append(cls(user))
            return messages
        return messages

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def is_valid(message):
        is_valid = True
        if len(message['message'])<5:
            flash ('Message must be at least 5 characters long !', 'messageSend')
            is_valid=False
        return is_valid

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM messages WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def delete_messages_by_user(cls, id):
        query = "DELETE FROM messages WHERE user_id = %(id)s;"
        data = {
            'user_id': id
        }
        connectToMySQL(cls.db_name).query_db(query, data)





"""
    @staticmethod
    def valid_message(message):
        valid_message = True
        query = "SELECT * FROM messages WHERE user_id = %(user_id)s;"
        results = connectToMySQL(Message.db_name).query_db(query,message)
        if len(valid_message['message'])<5:
            flash ('Message must have at least 5 characters !', 'messageValid')
        return valid_message

    @classmethod
    def get_user_sent_messages(cls, data):
        query = "SELECT messages.* FROM users LEFT JOIN messages ON users.id = messages.receiver_id LEFT JOIN users as users2 ON users2.id = messages.sender_id WHERE user.id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        message_count = []
        if results:
            for user in results:
                message_count.append(cls(user))
            return message_count
        return message_count

    @classmethod
    def get_message_by_user_id(cls,data):
        query = "SELECT * FROM messages WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False"""