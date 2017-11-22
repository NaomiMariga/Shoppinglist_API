import random
import smtplib

from sqlalchemy.sql import text
from validate_email import validate_email

from models.utilities import Utilities


class User(Utilities):
    def check_email_exists(self, email):
        try:
            sql = "SELECT COUNT(email) AS emails FROM users WHERE email= :email"
            connection = self.database_connection()
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

                                    sql = "INSERT INTO users (email, username, pword) VALUES (:email, :username, :pword)"
                                    connection = self.database_connection()
                                    stmt = text(sql)
                                    stmt = stmt.bindparams(email=email, username=username, pword=password)
                                    connection.execute(stmt)

                                    success = True
                                    message = "user added successfully"

                                else:
                                    message = "Password must contain uppercase, lowercase and digits"
                            else:
                                message = "password must be 6 or more characters in length"
                        else:
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
                    if password.strip():
                        sql = "SELECT email, username, user_id, pword FROM users WHERE email = :email AND pword =:pword"
                        connection = self.database_connection()
                        stmt = text(sql)
                        stmt = stmt.bindparams(email=email, pword=password)
                        result = connection.execute(stmt)
                        row = result.fetchone()

                        if row is not None:
                            success = True
                            user_id = row["user_id"]
                            username = row["username"]
                            auth_token = self.auth_token("abcdefghijklmnopqrstuvwzyz1234567890", 20)
                            message = {
                                "message": "Login was successful, Welcome " + username,
                                "user_id": user_id,
                                "auth_token": auth_token
                            }
                            sql = "INSERT INTO authentication (user_id, auth_token) VALUES (:user_id, :auth_token)"
                            stmt = text(sql)
                            stmt = stmt.bindparams(user_id=user_id, auth_token=auth_token)
                            connection.execute(stmt)
                        else:
                            message = "No match was found"
                    else:
                        message = "password has spaces"
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

    def send_email(self, receiver, subject, message):
        try:
            smtp = smtplib.SMTP("smtp.gmail.com", 587)  # initialize smtp class
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login("prettynoms@gmail.com", "shoppinglist1")
            header = 'To:' + receiver + '\nFrom: shopping list<prettynoms@gmail.com>\nSubject: ' + subject + '\n'
            msg = header + '\n' + message + '\n\n'
            smtp.sendmail("prettynoms@gmail.com", receiver, msg)
            smtp.close()
            return True
        except Exception:
            return False

    def reset_password(self, email):
        success = False
        try:
            if validate_email(email):
                if self.check_email_exists(email):
                    sql = "SELECT email, user_id, pword, username FROM users WHERE email = :email"
                    connection = self.database_connection()
                    stmt = text(sql)
                    stmt = stmt.bindparams(email=email)
                    result = connection.execute(stmt)
                    row = result.fetchone()

                    if row is not None:
                        email = row["email"]
                        user_id = row["user_id"]
                        print(user_id)
                        username = row["username"]
                        temp_password = self.auth_token("abcdefghijklmnopqrstuvwxyz", 10)
                        print(temp_password)
                        message_body = " Hi " + username + "\n Please use this temporary password to login in \n" + temp_password
                        if self.send_email(email, "Shoppinglist Password Reset", message_body):
                            sql = "UPDATE users SET pword = :temp_password WHERE user_id = :user_id "
                            stmt = text(sql)
                            stmt = stmt.bindparams(user_id=user_id, temp_password=temp_password)
                            print(temp_password)
                            connection = self.database_connection()
                            connection.execute(stmt)
                            success = True
                            message = "password was changed"
                        else:
                            message = "Error sending password reset email"
                    else:
                        message = "No match was found"
                else:
                    message = "email does not exist in our database"
            else:
                message = "invalid email format detected"
        except Exception as error:
            message = "An exception error occurred " + str(error)
        return {
            "success": success,
            "message": message
        }

    def user_is_logged_in(self, user_id, token):
        success = False
        try:
            sql = "SELECT COUNT(user_id) as cols FROM authentication WHERE user_id = :user_id AND auth_token = :auth_token"
            connection = self.database_connection()
            stmt = text(sql)
            stmt = stmt.bindparams(user_id=user_id, auth_token=token)
            result = connection.execute(stmt)
            row = result.fetchone()
            if row is not None:
                rows = row["cols"]
                if int(rows) > 0:
                    success = True
                    message = "user is logged in"
                else:
                    message = "User is not logged in"
            else:
                message = "User is not logged in"
        except Exception as error:
            message = "An exception error occurred" + str(error)
        return{
            "success": success,
            "message": message
        }

    def change_password(self, user_id, token, old_password, new_password):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                sql = "SELECT pword FROM users WHERE user_id = :user_id"
                connection = self.database_connection()
                stmt = text(sql)
                stmt = stmt.bindparams(user_id=user_id)
                result = connection.execute(stmt)
                row = result.fetchone()

                if row is not None:
                    if row["pword"] == old_password:
                        if new_password is not None and new_password.isalnum() and new_password.strip() is not "":
                            if any(letter.isdigit() for letter in new_password) and any(letter.islower() for letter in new_password) \
                               and any(letter.isupper() for letter in new_password):
                                if len(new_password) >= 6:
                                    sql = "UPDATE users SET pword = :pword WHERE user_id = :user_id"
                                    stmt = text(sql)
                                    stmt = stmt.bindparams(pword=new_password, user_id=user_id)
                                    connection.execute(stmt)
                                    success = True
                                    message = "password Changed successfully"
                                else:
                                    message = "password length should be at least 6 characters"
                            else:
                                message = "use mixed uppercase lowercase and numbers for a strong password"
                        else:
                            message = "password only contains letters and numbers and cannot be null or an empty string"
                    else:
                        message = "passwords do not match"
                else:
                    message = "No match found"
            else:
                message = "user must be logged in to perform this action"
        except Exception as error:
            message = "An exception error occurred" + str(error)
        return{
            "success": success,
            "message": message
        }

    def log_out(self, user_id, token):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                sql = "DELETE FROM authentication WHERE user_id = :user_id AND auth_token = :auth_token"
                connection = self.database_connection()
                stmt = text(sql)
                stmt = stmt.bindparams(user_id=user_id, auth_token=token)
                result = connection.execute(stmt)
                row = result.fetchone

                if row is not None:
                    success = True
                    message = "User successfully logged out"
                else:
                    message = "No match found, user is not logged in"
            else:
                message = "user must be logged in to perform this action"
        except Exception as error:
            message = "An exception error occurred " + str(error)
        return{
            "success": success,
            "message": message
        }
