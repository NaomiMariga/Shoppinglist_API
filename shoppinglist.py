"""
lists and items functions
"""
from sqlalchemy.sql import text

from user import User


class Shoppinglist(User):
    def create_shoppinglist(self, user_id, token, list_name: str):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                if list_name.strip() is not "":
                    if list_name is not None and len(list_name) >= 1:
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
                    message = "list name should not be an empty string"
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
                rows = result.fetchall()

                if rows is not None:
                    success = True
                    message = []
                    for row in rows:
                        success = True
                        user_id = row["user_id"]
                        list_id = row["list_id"]
                        list_name = row["list_name"]
                        update_time = str(row["time_updated"])
                        lists = {
                            "user_id": user_id,
                            "list_id": list_id,
                            "list_name": list_name,
                            "update_time": update_time
                        }
                        message.append(lists)
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
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                if list_name is not None and list_name.strip() is not "":
                    if list_name.isalnum() and len(list_name) >= 1:
                        sql = "UPDATE lists SET list_name = :list_name WHERE list_id = :list_id AND user_id = :user_id"
                        connection = self.database_connection()
                        stmt = text(sql)
                        stmt = stmt.bindparams(list_name=list_name, list_id=list_id, user_id=user_id)
                        connection.execute(stmt)
                        success = True
                        message = "list name successfully changed"
                    else:
                        message = "list name contains letters and numbers only and it is at least 1 character long"
                else:
                    message = "list name can not be null or an empty string"
            else:
                message = "user must be logged in to perform this action"
        except Exception as error:
            message = "An exception error occurred " + str(error)

        return{
            "success": success,
            "message": message
        }

    def delete_shoppinglist(self, user_id, token, list_id):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                sql = "DELETE FROM items WHERE list_id = :list_id"
                connection = self.database_connection()
                stmt = text(sql)
                stmt = stmt.bindparams(list_id=list_id)
                connection.execute(stmt)

                sql = "DELETE FROM lists WHERE list_id = :list_id AND user_id = :user_id"
                stmt = text(sql)
                stmt = stmt.bindparams(list_id=list_id, user_id=user_id)
                connection.execute(stmt)
                success = True
                message = "list deleted"
            else:
                message = "user must be logged in to perform this action"
        except Exception as error:
            message = "An exception error occurred " + str(error)
        return{
            "success": success,
            "message": message
        }

    def add_items(self, user_id, token, list_id, item_name, quantity, units, cost):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                if item_name is not None and item_name.strip() is not "" and len(item_name) >= 1:
                    sql = "INSERT INTO items (list_id, item_name, quantity, units, item_cost) VALUES (:list_id, :item_name," \
                          " :quantity, :units, :item_cost)"
                    connection = self.database_connection()
                    stmt = text(sql)
                    stmt = stmt.bindparams(list_id=list_id, item_name=item_name, quantity=quantity, units=units, item_cost=cost)
                    connection.execute(stmt)
                    success = True
                    message = "item added successfully"
                else:
                    message = "item name is not an empty string, not null and is at least 1 character long"
            else:
                message = "user must be logged in to perform this action"
        except Exception as error:
            message = "An exception error occurred " + str(error)

        return{
            "success": success,
            "message": message
        }

    def read_items(self, user_id, token, list_id):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                sql = "SELECT * FROM items WHERE list_id = :list_id"
                connection = self.database_connection()
                stmt = text(sql)
                stmt = stmt.bindparams(list_id=list_id)
                result = connection.execute(stmt)
                rows = result.fetchall()
                if rows is not None:
                    success = True
                    message = []
                    for row in rows:
                            item_id = row["item_id"]
                            list_id = row["list_id"]
                            item_name = row["item_name"]
                            quantity = row["quantity"]
                            units = row["units"]
                            item_cost = row["item_cost"]
                            update_time = str(row["time_updated"])
                            items = {
                                "item_id": item_id,
                                "list_id": list_id,
                                "item_name": item_name,
                                "quantity": quantity,
                                "units": units,
                                "item_cost": item_cost,
                                "update_time": update_time
                            }
                            message.append(items)
                else:
                    message = "No match found"
            else:
                message = "user must be logged in to carry out this action"
        except Exception as error:
            message = "An exception error occurred " + str(error)
        return{
            "success": success,
            "message": message
        }

    def edit_items(self, user_id, token, list_id, item_id, attribute, value):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                if attribute == "item_name":
                    if value is not None and value.strip() is not "":
                        sql = "UPDATE items SET item_name = :item_name WHERE item_id = :item_id AND list_id=:list_id"
                        stmt = text(sql)
                        stmt = stmt.bindparams(list_id=list_id, item_id=item_id, item_name=value)
                        connection = self.database_connection()
                        connection.execute(stmt)
                        success = True
                        message = attribute + " Updated successfully"
                    else:
                        message = "value and attribute cannot be none or empty string "
                elif attribute == "quantity":
                    if value is None:
                        value = 0
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            value = 0
                    sql = "UPDATE items SET quantity = :quantity WHERE item_id = :item_id AND list_id=:list_id"
                    stmt = text(sql)
                    stmt = stmt.bindparams(list_id=list_id, item_id=item_id, quantity=value)
                    connection = self.database_connection()
                    connection.execute(stmt)
                    success = True
                    message = attribute + "Updated successfully"
                elif attribute == "units":
                    sql = "UPDATE items SET units = :units WHERE item_id = :item_id AND list_id=:list_id"
                    stmt = text(sql)
                    stmt = stmt.bindparams(list_id=list_id, item_id=item_id, units=value)
                    connection = self.database_connection()
                    connection.execute(stmt)
                    success = True
                    message = attribute + "Updated successfully"
                elif attribute == "cost":
                    sql = "UPDATE items SET item_cost = :item_cost WHERE item_id = :item_id AND list_id=:list_id"
                    stmt = text(sql)
                    stmt = stmt.bindparams(list_id=list_id, item_id=item_id, item_cost=value)
                    connection = self.database_connection()
                    connection.execute(stmt)
                    success = True
                    message = attribute + "Updated successfully"
                else:
                    message = "unknown attribute"
            else:
                message = "user must be logged in to perform this action"
        except Exception as error:
            message = "An exception error occurred " + str(error)
        return{
               "success": success,
               "message": message
               }

    def delete_items(self, user_id, token, list_id, item_id):
        success = False
        try:
            logged_in = self.user_is_logged_in(user_id, token)
            if logged_in["success"]:
                sql = "DELETE FROM items WHERE list_id =:list_id and item_id = :item_id"
                connection = self.database_connection()
                stmt = text(sql)
                stmt = stmt.bindparams(list_id=list_id, item_id=item_id)
                connection.execute(stmt)
                success = True
                message = "item deleted successfully"
            else:
                message = "user must be logged in to perform this action"

        except Exception as error:
            message = "An exception error occurred " + str(error)
        return{
            "success": success,
            "message": message
        }
