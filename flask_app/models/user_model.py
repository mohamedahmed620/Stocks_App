from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.companies_model import Companies

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class user:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def register_function(cls, data):
        query = "insert into users_table (first_name,last_name, email, password) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        results = MySQLConnection("Stocks_project").query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * from users_table where email = %(email)s;"
        results = MySQLConnection("Stocks_project").query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def user_info(cls, data):
        query = "SELECT * from users_table where id = %(id)s;"
        results = MySQLConnection("Stocks_project").query_db(query, data)

        if not results:
            return False
        return results[0]['first_name']
    
    @staticmethod
    def validate_register(data):
        query = "select * from users_table where email = %(email)s;"
        results = MySQLConnection("Stocks_project").query_db(query, data)
        is_valid = True
        if len(data["first_name"]) <3:
            flash("please enter valid First Name, First name should be longer than 3 leters", "register")
            is_valid = False
        if len(data["last_name"]) <3:
            flash("please enter valid Last Name, last name should be longer than 3 leters", "register")
            is_valid = False
        if len(data["password"]) <8:
            flash("please enter another Password, Password length should be more than 8 characters", "register")
            is_valid = False
        if data["confirm"] != data["password"]:
            flash("please enter the same password on confirm password", "register")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("please Enter a valid Email", "register")
            is_valid = False
        if len(results) >0: 
            flash("please Choose another Email", "register")
            is_valid = False
        return is_valid

    
        

    