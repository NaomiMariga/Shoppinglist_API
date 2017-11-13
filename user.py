import random
from sqlalchemy.sql import text
from validate_email import validate_email
from utilities import Utilities


class User(Utilities):
    def check_email_exists(self, email):
        try:
            sql = "SELECT COUNT(email) AS emails FROM users WHERE email= :email"
            connection, metadata = self.database_connection()
            stmt = text(sql)
            stmt = stmt.bindparams(email=email)
            result = connection.execute(stmt)
            row = result.fetchone()
            if row is not None:
                if int(row["emails"]) > 0:
                    return True

        except Exception as e:
            print(str(e))
        return False

    def user_registration(self, email, username, password):
        success = False
        try:
            if validate_email(email):
                if not self.check_email_exists(email):
                    if username.isalnum() and len(username) >= 3 and username.strip is not "":
                        if password is not None and password.isalnum() and password.strip() is not "":
                            if len(password) >= 6:
                                if any(letter.isupper()for letter in password) and any(letter.islower() for letter in password) \
                                   and any(letter.isdigit() for letter in password):

                                    sql = "INSERT INTO users (email, username, pword) VALUES (:email, :username :pword)"
                                    connection, metadata = self.database_connection()
                                    stmt = text(sql)
                                    stmt = stmt.bindparams(email=email, username=username, pword=password)
                                    connection.execute(stmt)

                                    success = True
                                    message = "user added successfully"

                                else:
                                    message = "Password must contain uppercase, lowercase and digits"
                            else:
                                message = "password must be 6 or more characters in length"
                        message = "password contains only letters and numbers and it should be not null or an empty string"
                    else:
                        message = "username contains only letters and numbers, at least 3 characters long and it can not be empty"
                else:
                    message = "Email is already registered, try login"
            else:
                message = "invalid email format is not allowed"
        except Exception as error:
            print(str(error))
            message = "An exception error occurred" + str(error)
        return {
            "success": success,
            "message": message
        }

    def auth_token(self, characters, length):
        out = "".join(random.sample(characters, length))
        return out

    def user_login(self, email, password):
        success = False
        try:
            if validate_email(email):
                if self.check_email_exists(email):
                    if password:
                        sql = "SELECT email, username, user_id, pword FROM users WHERE email == :email AND pword ==:pword"
                        connection, metadata = self.database_connection()
                        stmt = text(sql)
                        stmt = stmt.bindparams(email=email, pword=password)
                        result = connection.execute(stmt)
                        row = result.fetchone()

                        if row is not None:
                            success = True
                            user_id = row["user_id"]
                            auth_token = self.auth_token("abcdefghijklmnopqrstuvwzyz1234567890", 20)
                            message = {
                                "message": "Login was successful, Welcome" + row["username"],
                                "user_id" : row["user_id"],
                                "token": auth_token
                            }
                            sql = "INSERT INTO authentication (user_id, auth_token) VALUES (:user_id, :auth_token)"
                            stmt = text(sql)
                            stmt = stmt.bindparams(user_id=user_id, auth_token=auth_token)
                            connection.execute(stmt)
                        else:
                            message = "No match was found"
                    else:
                        message = "provide password"
                else:
                    message = "Email is not registered with us"
            else:
                message = "Email format is invalid"
        except Exception as error:
            print(str(error))
            message = "An exception error occurred" + str(error)
        return{
            "success": success,
            "message": message
        }

    def reset_password(self, email):
        return

    def token(self):
        return

    def user_is_logged_in(self, user_id, token):
        return

    def change_password(self, user_id, token, old_password, new_password):
        return

    def log_out(self, user_id, token):
        return
