"""
lists and items functions
"""
from sqlalchemy.sql import text

from user import User


class Shoppinglist(User):

    def create_shoppinglist(self, user_id, token, list_name:str):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                if list_name.isalnum() and list_name.strip() is not "":
                    if list_name is not None and len(list_name) > 1:
                        sql = "INSERT INTO lists (user_id, list_name) VALUES (:user_id, :list_name)"
                        connection = self.database_connection()
                        stmt = text(sql)
                        stmt = stmt.bindparams(user_id=user_id, list_name=list_name)
                        connection.execute(stmt)
                        success = True
                        message = "List successfully created"
                    else:
                        message = "list name should not be null and should be at least 1 character long"
                else:
                    message = "list name should be alphanumeric and should not be an empty string"
            else:
                message = "user must be logged in to add a list"
        except Exception as error:
            message = "An exception error occurred" + str(error)
        return{
            "success": success,
            "message": message
        }

    def read_shoppinglist(self, user_id, token):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                sql = "SELECT * FROM lists WHERE user_id = :user_id"
                connection = self.database_connection()
                stmt = text(sql)
                stmt = stmt.bindparams(user_id=user_id)
                result = connection.execute(stmt)
                row = result.fetchAll()

                if row is not None:
                    success = True
                    user_id = row["user_id"]
                    list_id = row["list_id"]
                    list_name = row["list_name"]
                    update_time = row["time_updated"]
                    message = []
                    lists = {
                        "user_id": user_id,
                        "list_id": list_id,
                        "list_name": list_name,
                        "update_time": update_time
                    }
                    message = message.append(lists)
                else:
                    message = "No lists found"
            else:
                message = "User must be logged in to perform this action"
        except Exception as error:
            message = "An exception error occurred " + str(error)
        return{
            "success": success,
            "message": message
        }

    def edit_shoppinglist(self, user_id, token, list_id, list_name):
        return

    def delete_shoppinglist(self, user_id, token, list_id):
        return

    def add_items(self, user_id, token, list_id, item_name, quantity, units, cost):
        return

    def read_items(self, user_id, token, list_id):
        return

    def edit_items(self, user_id, token, list_id, item_id, attribute, value):
        return

    def delete_items(self, user_id, token, list_id, item_id):
        return
