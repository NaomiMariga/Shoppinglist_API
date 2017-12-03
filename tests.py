import unittest

from models.shoppinglist import Shoppinglist
from models.user import User
from sqlalchemy.sql import text


class Tests(unittest.TestCase):

    user = User()
    shopping = Shoppinglist()
    """
    items =None
    list = None
    auth_token = None
    user_id = None
    """
    @classmethod
    def setUpClass(cls):
        cls.registered_email ="kaburamariga@gmail.com"
        cls.registered_password = "Password1234"
        print(cls.registered_email, " and ", cls.registered_password)

    def test_13_all_functions_return_a_dictionary(self):
        self.assertIsInstance(self.user.user_registration(None, None, None), dict, "registration returns a dictionary")
        self.assertIsInstance(self.user.user_login(None, None), dict, "login returns a dictionary")
        self.assertIsInstance(self.user.user_is_logged_in(None, None), dict, " logged_in returns True or False")
        self.assertIsInstance(self.user.reset_password(None), dict, " reset_password returns a dictionary")
        self.assertIsInstance(self.user.change_password(None, None, None, None), dict, " change_password returns a dictionary")
        self.assertIsInstance(self.user.log_out(None, None), dict, " logout returns a dictionary")
        self.assertIsInstance(self.shopping.create_shoppinglist(None, None, None), dict, "create shoppinglist returns dict")
        self.assertIsInstance(self.shopping.read_shoppinglist(None, None), dict, "Read shoppinglist returns dictionary")
        self.assertIsInstance(self.shopping.edit_shoppinglist(None, None, None, None), dict, "edit shoppinglist returns dictionary")
        self.assertIsInstance(self.shopping.add_items(None, None, None, None, None, None, None), dict, "Add items returns dict")
        self.assertIsInstance(self.shopping.read_items(None, None, None), dict, "read items returns a dictionary")
        self.assertIsInstance(self.shopping.edit_items(None, None, None, None, None, None), dict, "edit items returns a dictionary")
        self.assertIsInstance(self.shopping.delete_items(None, None, None, None), dict, "delete items returns dictionary")
        self.assertIsInstance(self.shopping.delete_shoppinglist(None, None, None), dict, "delete list returns a dictionary")

    def test_01_register_input_validation_works_as_expected(self):
        result1 = self.user.user_registration("email", "username", self.registered_password)
        result2 = self.user.user_registration("example@email.com", "username", "pass")
        result3 = self.user.user_registration("example@email.com", "username", "password1234")
        result4 = self.user.user_registration("example@email.com", "", self.registered_password)
        result5 = self.user.user_registration("example@email.com", "username", "")
        result6 = self.user.user_registration("example@email.com", "us", self.registered_password)
        result7 = self.user.user_registration("example@email.com", "username", "Password")
        print(self.registered_password, self.registered_email, "Registration point")
        result8 = self.user.user_registration(self.registered_email, "username", self.registered_password)
        self.assertFalse(result1["success"], "Registration only accepts a valid email format")
        self.assertFalse(result2["success"], "Registration accepts a password length of at least 6 characters")
        self.assertFalse(result3["success"], "Registration Accepts password mixed with uppercase and lowercase")
        self.assertFalse(result4["success"], "Registration does not take username as a empty string")
        self.assertFalse(result5["success"], "Registration does not take password as an empty string")
        self.assertFalse(result6["success"], "Registration does not accept a username less than 3 characters")
        self.assertFalse(result7["success"], "Registration Accepts passwords that are mixed with letters and numbers")
        self.assertTrue(result8["success"], "Registration should be successful")

    def test_02_login_accepts_only_registered_parties(self):
        result1 = self.user.user_login("email", self.registered_password)
        result2 = self.user.user_login("registered@email.com", "password")
        result3 = self.user.user_login("unregistered1@email.com", self.registered_password)
        result4 = self.user.user_login(self.registered_email, self.registered_password)
        self.assertFalse(result1["success"], "Incorrect email format is not allowed")
        self.assertFalse(result2["success"], "Incorrect password is not allowed")
        self.assertFalse(result3["success"], "Unregistered email is not authorised")
        print(self.registered_email, self.registered_password, "Login point")
        self.assertTrue(result4["success"], "login should be successful")
        self.__class__.auth_token = result4["message"]["auth_token"]
        self.__class__.user_id = result4["message"]["user_id"]
        self.assertIsInstance(result4["message"], dict, "returns a dictionary")
        print(self.__class__.auth_token, self.__class__.user_id)

    def test_03_logged_in_functions_properly(self):
        print(self.__class__.user_id, self.__class__.auth_token)
        result1 = self.user.user_is_logged_in(self.user_id, "token")
        result2 = self.user.user_is_logged_in("user_id", self.auth_token)
        result3 = self.user.user_is_logged_in(self.user_id, self.auth_token)
        self.assertFalse(result1["success"], "Does not accept wrong token")
        self.assertFalse(result2["success"], "Does not accept wrong user_id")
        self.assertTrue(result3["success"], "Accepts correct user_id and token")

    def test_04_create_shoppinglist(self):
        result1 = self.shopping.create_shoppinglist(None, None, "listName")
        result2 = self.shopping.create_shoppinglist("", "", "listName")
        result3 = self.shopping.create_shoppinglist("user_id", "token", "listName")
        result4 = self.shopping.create_shoppinglist(self.user_id, self.auth_token, "")
        result5 = self.shopping.create_shoppinglist(self.user_id, self.auth_token, None)
        result7 = self.shopping.create_shoppinglist(self.user_id, self.auth_token, "listName")
        self.assertFalse(result1["success"], "user_id and token cannot be None")
        self.assertFalse(result2["success"], "user_id and token cannot be empty strings")
        self.assertFalse(result3["success"], "user_id and token cannot be incorrect")
        self.assertFalse(result4["success"], "listName cannot be an empty string")
        self.assertFalse(result5["success"], "listName cannot be None")
        self.assertTrue(result7["success"], "List should be successfully created")

    def test_05_read_shoppinglist(self):
        result1 = self.shopping.read_shoppinglist(None, None)
        result2 = self.shopping.read_shoppinglist("", "")
        result3 = self.shopping.read_shoppinglist("user_id", "token")
        result4 = self.shopping.read_shoppinglist(self.user_id, self.auth_token)
        self.assertFalse(result1["success"], "user_id and token cannot be none")
        self.assertFalse(result2["success"], "user_id and token cannot be empty strings")
        self.assertFalse(result3["success"], "user_id and token cannot be incorrect")
        self.assertTrue(result4["success"], "Should read available lists")
        self.__class__.list = result4["message"][0]
        self.assertIsInstance(result4["message"], list, "expected to return  a dictionary")
        self.assertIsInstance(self.list, dict, "expects a list of shoppingLists")
        self.__class__.list_id = self.list["list_id"]
        print("list_id:", self.list_id)

    def test_06_add_items(self):
        result1 = self.shopping.add_items(self.user_id, self.auth_token, self.list["list_id"], "", "", "", "")
        result2 = self.shopping.add_items(None, None, None, None, None, None, None)
        result3 = self.shopping.add_items(self.user_id, self.auth_token, self.list["list_id"], "itemName", None, "", None)
        self.assertFalse(result1["success"], "listName cannot be empty string")
        self.assertFalse(result2["success"], "user_id, token and listName cannot be null")
        self.assertTrue(result3["success"], "item should be added")
        print(self.list, self.list["list_id"])

    def test_07_read_items(self):
        result1 = self.shopping.read_items(None, None, None)
        result2 = self.shopping.read_items("", "", "")
        result3 = self.shopping.read_items("user_id", "token", "list_id")
        result4 = self.shopping.read_items(self.user_id, self.auth_token, self.list["list_id"])
        self.assertFalse(result1["success"], "user_id, token and list_id cannot be null")
        self.assertFalse(result2["success"], "user_id, token and list_id cannot be empty strings")
        self.assertFalse(result3["success"], "user_id, token and list_id cannot be incorrect")
        self.assertTrue(result4["success"], "should read_items")
        self.__class__.items = result4["message"][0]
        self.assertIsInstance(result4["message"], list, "Expected to be a list")
        self.assertIsInstance(self.items, dict, "Expected to be a dict")
        self.__class__.item_id = self.items["item_id"]
        print("item_id:", self.item_id)

    def test_08_edit_shoppinglist(self):
        result1 = self.shopping.edit_shoppinglist(None, None, None, None)
        result2 = self.shopping.edit_shoppinglist("", "", "", "")
        result3 = self.shopping.edit_shoppinglist("user_id", "token", "list_id", "newListName")
        result4 = self.shopping.edit_shoppinglist(self.user_id, self.auth_token, self.list["list_id"], "newListName")
        self.assertFalse(result1["success"], "user_id, token, list_id and list_name cannot be null")
        self.assertFalse(result2["success"], "user_id, token , list_name and list_id cannot be empty strings")
        self.assertFalse(result3["success"], "Incorrect user_id, token and list_id is not allowed")
        self.assertTrue(result4["success"], "editing list should be successful")

    def test_09_edit_items(self):
        result1 = self.shopping.edit_items(None, None, None, None, None, None)
        result2 = self.shopping.edit_items("", "", "", "", "", "")
        result3 = self.shopping.edit_items("user_id", "token", "list_id", "item_id", "attribute", "value")
        result4 = self.shopping.edit_items(self.user_id, self.auth_token, self.items["list_id"], self.items["item_id"], "item_name", "value")
        self.assertFalse(result1["success"], "user_id, token, list_id, item_id, attribute and value cannot be null ")
        self.assertFalse(result2["success"], "user_id, token, list_id, item_id, attribute and value cannot be empty strings")
        self.assertFalse(result3["success"], "user_id, token, list_id and item_id cannot be be incorrect")
        self.assertTrue(result4["success"], "Should edit successfully")
        print(self.items, self.items["item_id"])


    def test_10_delete_items(self):
        result1 = self.shopping.delete_items("", "", "", "")
        result2 = self.shopping.delete_items(None, None, None, None)
        result3 = self.shopping.delete_items("user_id", "token", "list_id", "item_id")
        result4 = self.shopping.delete_items(self.user_id, self.auth_token, self.items["list_id"], self.items["item_id"])
        self.assertFalse(result1["success"], "user_id, token, list_id, item_id cannot be empty strings")
        self.assertFalse(result2["success"], "user_id, token, list_id, item_id cannot be null")
        self.assertFalse(result3["success"], "user_id, token, list_id, item_id cannot be incorrect")
        self.assertTrue(result4["success"], "delete_item should delete successfully")

    def test_11_delete_shopping(self):
        result1 = self.shopping.delete_shoppinglist(None, None, None)
        result2 = self.shopping.delete_shoppinglist("", "", "")
        result3 = self.shopping.delete_shoppinglist("user_id", "token", "list_id")
        result4 = self.shopping.delete_shoppinglist(self.user_id, self.auth_token, self.list["list_id"])
        self.assertFalse(result1["success"], "user_id, token and list_id cannot be null")
        self.assertFalse(result2["success"], "user_id, token and list_id cannot be empty strings")
        self.assertFalse(result3["success"], "user_id, token and list_id cannot be incorrect")
        self.assertTrue(result4["success"], "delete list should be successful")

    def test_12_change_password(self):
            result1 = self.user.change_password(None, None, self.registered_password, "NewPassword1234")
            result2 = self.user.change_password("", "", self.registered_password, "Newpassword123")
            result3 = self.user.change_password("user_id", "token", self.registered_password, "Newpassword1234")
            result4 = self.user.change_password(self.user_id, self.auth_token, "oldPassword1234", "Newpassword1234")
            result5 = self.user.change_password(self.user_id, self.auth_token, self.registered_password, "Password")
            result6 = self.user.change_password(self.user_id, self.auth_token, self.registered_password, "Pass")
            result7 = self.user.change_password(self.user_id, self.auth_token, self.registered_password, "newpassword1234")
            result8 = self.user.change_password(self.user_id, self.auth_token, self.registered_password, self.registered_password)
            self.assertFalse(result1["success"], "Change password does not accept noneType user_id and token")
            self.assertFalse(result2["success"], "change password must be provided with user_id and token")
            self.assertFalse(result3["success"], "change password does not accept incorrect user_id and token")
            self.assertFalse(result4["success"], "change password does not accept incorrect old password")
            self.assertFalse(result5["success"], "change password does not accept a new password without mixed letters and numbers")
            self.assertFalse(result6["success"], "change password does not accept new pass of less than 6 characters")
            self.assertFalse(result7["success"], "change password does not accept new password without mixed uppercase and lowercase")
            self.assertTrue(result8["success"], "change password should be successful")

    def test_14_logout(self):
            result1 = self.user.log_out(None, None)
            result2 = self.user.log_out("", "")
            result3 = self.user.log_out("user_id", "token")
            result4 = self.user.log_out(self.user_id, self.auth_token)
            self.assertFalse(result1["success"], "user_id and token can not be none")
            self.assertFalse(result2["success"], "user_id and token cannot be empty strings")
            self.assertFalse(result3["success"], "user_id and token cannot be incorrect")
            self.assertTrue(result4["success"], "logout should be True")

    def test_15_reset_password(self):
                result1 = self.user.reset_password("email")
                result2 = self.user.reset_password("example@email.com")
                result3 = self.user.reset_password(self.registered_email)
                self.assertFalse(result1["success"], "invalid email format is not allowed")
                self.assertFalse(result2["success"], "does not accept unregistered email")
                self.assertTrue(result3["success"], "Email should be sent")

    @classmethod
    def tearDownClass(cls):

        connect = cls.user.database_connection()
        sql = "DELETE FROM items WHERE list_id = :list_id and item_id = :item_id"
        stmt = text(sql)
        stmt = stmt.bindparams(list_id=cls.list["list_id"], item_id=cls.items["item_id"])
        connect.execute(stmt)

        sql = "DELETE FROM lists WHERE user_id = :user_id and list_id = :list_id"
        stmt = text(sql)
        stmt = stmt.bindparams(user_id=cls.user_id, list_id=cls.list["list_id"])
        connect.execute(stmt)

        sql = "DELETE FROM authentication WHERE user_id = :user_id and auth_token= :auth_token"
        stmt = text(sql)
        stmt = stmt.bindparams(user_id=cls.user_id, auth_token=cls.auth_token)
        connect.execute(stmt)

        sql = "DELETE FROM users WHERE user_id = :user_id and email = :email"
        stmt = text(sql)
        stmt = stmt.bindparams(email=cls.registered_email, user_id=cls.user_id)
        connect.execute(stmt)

        print(cls.registered_email, " and ", cls.registered_password)
        print("its working", cls.user_id)


if __name__ == '__main__':
    unittest.main()
