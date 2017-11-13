import unittest

from shoppinglist import Shoppinglist

from user import User

user = User()
shopping = Shoppinglist(user)


class Tests(unittest.TestCase):
    auth_token = None
    user_id = None
    list = None
    items = None

    def test_all_functions_return_a_dictionary(self):
        self.assertIsInstance(user.user_registration(None, None, None), dict, "registration returns a dictionary")
        self.assertIsInstance(user.user_login(None, None), dict, "login returns a dictionary")
        self.assertIsInstance(user.user_is_logged_in(None, None, None), bool, " logged_in returns True or False")
        self.assertIsInstance(user.reset_password(None), dict, " reset_password returns a dictionary")
        self.assertIsInstance(user.change_password(None, None, None, None), dict, " change_password returns a dictionary")
        self.assertIsInstance(user.log_out(None, None, None), bool, " logout returns a True or False")
        self.assertIsInstance(shopping.create_shoppinglist(None, None, None), dict, "create shoppinglist returns dict")
        self.assertIsInstance(shopping.read_shoppinglist(None, None), dict, "Read shoppinglist returns dictionary")
        self.assertIsInstance(shopping.edit_shoppinglist(None, None, None, None), dict, "edit shoppinglist returns dictionary")
        self.assertIsInstance(shopping.add_items(None, None, None, None, None, None, None), dict, "Add items returns dict")
        self.assertIsInstance(shopping.read_items(None, None, None), dict, "read items returns a dictionary")
        self.assertIsInstance(shopping.edit_items(None, None, None, None, None, None), dict, "edit items returns a dictionary")
        self.assertIsInstance(shopping.delete_items(None, None, None, None), dict, "delete items returns dictionary")
        self.assertIsInstance(shopping.delete_shoppinglist(None, None, None), dict, "delete list returns a dictionary")

    def test_register_input_validation_works_as_expected(self):
        result1 = user.user_registration("email", "username", "Password1234")
        result2 = user.user_registration("example@email.com", "username", "pass")
        result3 = user.user_registration("example@email.com", "username", "password1234")
        result4 = user.user_registration("example@email.com", "", "Password1234")
        result5 = user.user_registration("example@email.com", "username", "")
        result6 = user.user_registration("example@email.com", "us", "Password1234")
        result7 = user.user_registration("example@email.com", "username", "Password")
        result8 = user.user_registration("registered@email.com", "username", "Password1234")
        self.assertFalse(result1["success"], "Registration only accepts a valid email format")
        self.assertFalse(result2["success"], "Registration accepts a password length of at least 6 characters")
        self.assertFalse(result3["success"], "Registration Accepts password mixed with uppercase and lowercase")
        self.assertFalse(result4["success"], "Registration does not take username as a empty string")
        self.assertFalse(result5["success"], "Registration does not take password as an empty string")
        self.assertFalse(result6["success"], "Registration does not accept a username less than 3 characters")
        self.assertFalse(result7["success"], "Registration Accepts passwords that are mixed with letters and numbers")
        self.assertTrue(result8["success"], "Registration should be successful")

    def test_login_accepts_only_registered_parties(self):
        result1 = user.user_login("email", "Password1234")
        result2 = user.user_login("registered@email.com", "password")
        result3 = user.user_login("unregistered@email.com", "Password1234")
        result4 = user.user_login("registered@email.com", "Password1234")
        self.assertFalse(result1["success"], "Incorrect email format is not allowed")
        self.assertFalse(result2["success"], "Incorrect password is not allowed")
        self.assertFalse(result3["success"], "Unregistered email is not authorised")
        self.assertTrue(result4["success"], "login should be successful")
        self.__class__.auth_token = result4["message"]["auth_token"]
        self.__class__.user_id = result4["message"]["user_id"]
        self.assertIsInstance(result4["message"], dict, "returns a dictionary")

    def test_logged_in_functions_properly(self):
        result1 = user.user_is_logged_in(self.user_id, "token")
        result2 = user.user_is_logged_in("user_id", self.auth_token)
        result3 = user.user_is_logged_in(self.user_id, self.auth_token)
        self.assertFalse(result1["success"], "Does not accept wrong token")
        self.assertFalse(result2["success"], "Does not accept wrong user_id")
        self.assertTrue(result3["success"], "Accepts correct user_id and token")

    def test_reset_password(self):
        result1 = user.reset_password("email")
        result2 = user.reset_password("example@email.com")
        result3 = user.reset_password("registered@email.com")
        self.assertFalse(result1["success"], "invalid email format is not allowed")
        self.assertFalse(result2["success"], "does not accept unregistered email")
        self.assertTrue(result3["success"], "Email should be sent")

    def test_change_password(self):
        result1 = user.change_password(None, None, "Password1234", "NewPassword1234")
        result2 = user.change_password("", "", "Password1234", "Newpassword123")
        result3 = user.change_password("user_id", "token", "Password1234", "Newpassword1234")
        result4 = user.change_password(self.user_id, self.auth_token, "oldPassword1234", "Newpassword1234")
        result5 = user.change_password(self.user_id, self.auth_token, "Password1234", "Password")
        result6 = user.change_password(self.user_id, self.auth_token, "Password1234", "Pass")
        result7 = user.change_password(self.user_id, self.auth_token, "Password1234", "newpassword1234")
        result8 = user.change_password(self.user_id, self.auth_token, "Password1234", "Newpassword1234")
        self.assertFalse(result1["success"], "Change password does not accept noneType user_id and token")
        self.assertFalse(result2["success"], "change password must be provided with user_id and token")
        self.assertFalse(result3["success"], "change password does not accept incorrect user_id and token")
        self.assertFalse(result4["success"], "change password does not accept incorrect old password")
        self.assertFalse(result5["success"], "change password does not accept a new password without mixed letters and numbers")
        self.assertFalse(result6["success"], "change password does not accept new pass of less than 6 characters")
        self.assertFalse(result7["success"], "change password does not accept new password without mixed uppercase and lowercase")
        self.assertTrue(result8["success"], "change password should be successful")

    def test_logout(self):
        result1 = user.log_out(None, None)
        result2 = user.log_out("", "")
        result3 = user.log_out("user_id", "token")
        result4 = user.log_out(self.user_id, self.auth_token)
        self.assertFalse(result1["success"], "user_id and token can not be none")
        self.assertFalse(result2["success"], "user_id and token cannot be empty strings")
        self.assertFalse(result3["success"], "user_id and token cannot be incorrect")
        self.assertTrue(result4["success"], "logout should be True")

    def test_create_shoppinglist(self):
        result1 = shopping.create_shoppinglist(None, None, "listName")
        result2 = shopping.create_shoppinglist("", "", "listName")
        result3 = shopping.create_shoppinglist("user_id", "token", "listName")
        result4 = shopping.create_shoppinglist(self.user_id, self.auth_token, "")
        result5 = shopping.create_shoppinglist(self.user_id, self.auth_token, None)
        result6 = shopping.create_shoppinglist(self.user_id, self.auth_token, "@#$")
        result7 = shopping.create_shoppinglist(self.user_id, self.auth_token, "listName")
        self.assertFalse(result1["success"], "user_id and token cannot be None")
        self.assertFalse(result2["success"], "user_id and token cannot be empty strings")
        self.assertFalse(result3["success"], "user_id and token cannot be incorrect")
        self.assertFalse(result4["success"], "listName cannot be an empty string")
        self.assertFalse(result5["success"], "listName cannot be None")
        self.assertFalse(result6["success"], "listName accepts only alphanumeric")
        self.assertTrue(result7["success"], "List should be successfully created")

    def test_read_shoppinglist(self):
        result1 = shopping.read_shoppinglist(None, None)
        result2 = shopping.read_shoppinglist("", "")
        result3 = shopping.read_shoppinglist("user_id", "token")
        result4 = shopping.read_shoppinglist(self.user_id, self.auth_token)
        self.assertFalse(result1["success"], "user_id and token cannot be none")
        self.assertFalse(result2["success"], "user_id and token cannot be empty strings")
        self.assertFalse(result3["success"], "user_id and token cannot be incorrect")
        self.assertTrue(result4["success"], "Should read available lists")
        self.__class__.list = result4["message"][0]
        self.assertIsInstance(result4["message"], list, "expected to return  a dictionary")
        self.assertIsInstance(self.list, dict, "expects a list of shoppingLists")

    def test_add_items(self):
        result1 = shopping.add_items(self.user_id, self.auth_token, self.list["list_id"], "", "", "", "")
        result2 = shopping.add_items(None, None, None, None, None, None, None)
        result3 = shopping.add_items(self.user_id, self.auth_token, self.list["list_id"], "itemName", "", "", "")
        self.assertFalse(result1["success"], "listName cannot be empty string")
        self.assertFalse(result2["success"], "user_id, token and listName cannot be null")
        self.assertTrue(result3["success"], "item should be added")

    def test_read_items(self):
        result1 = shopping.read_items(None, None, None)
        result2 = shopping.read_items("", "", "")
        result3 = shopping.read_items("user_id", "token", "list_id")
        result4 = shopping.read_items(self.user_id, self.auth_token, self.list["list_id"])
        self.assertFalse(result1["success"], "user_id, token and list_id cannot be null")
        self.assertFalse(result2["success"], "user_id, token and list_id cannot be empty strings")
        self.assertFalse(result3["success"], "user_id, token and list_id cannot be incorrect")
        self.assertTrue(result4["success"], "should read_items")
        self.__class__.items = result4["message"][0]
        self.assertIsInstance(result4["message"], list, "Expected to be a list")
        self.assertIsInstance(self.items, dict, "Expected to be a dict")

    def test_edit_shoppinglist(self):
        result1 = shopping.edit_shoppinglist(None, None, None, None)
        result2 = shopping.edit_shoppinglist("", "", "", "")
        result3 = shopping.edit_shoppinglist("user_id", "token", "list_id", "newListName")
        result4 = shopping.edit_shoppinglist(self.user_id, self.auth_token, self.list["list_id"], "newListName")
        self.assertFalse(result1["success"], "user_id, token, list_id and list_name cannot be null")
        self.assertFalse(result2["success"], "user_id, token , list_name and list_id cannot be empty strings")
        self.assertFalse(result3["success"], "Incorrect user_id, token and list_id is not allowed")
        self.assertTrue(result4["success"], "editing list should be successful")

    def test_edit_items(self):
        result1 = shopping.edit_items(None, None, None, None, None, None)
        result2 = shopping.edit_items("", "", "", "", "", "")
        result3 = shopping.edit_items("user_id", "token", "list_id", "item_id", "attribute", "value")
        result4 = shopping.edit_items(self.user_id, self.auth_token, self.items["list_id"], self.items["item_id"], "attribute", "value")
        self.assertFalse(result1["success"], "user_id, token, list_id, item_id, attribute and value cannot be null ")
        self.assertFalse(result2["success"], "user_id, token, list_id, item_id, attribute and value cannot be empty strings")
        self.assertFalse(result3["success"], "user_id, token, list_id and item_id cannot be be incorrect")
        self.assertTrue(result4["success"], "Should edit successfully")

    def test_delete_items(self):
        result1 = shopping.delete_items("", "", "", "")
        result2 = shopping.delete_items(None, None, None, None)
        result3 = shopping.delete_items("user_id", "token", "list_id", "item_id")
        result4 = shopping.delete_items(self.user_id, self.auth_token, self.items["list_id"], self.items["item_id"])
        self.assertFalse(result1["success"], "user_id, token, list_id, item_id cannot be empty strings")
        self.assertFalse(result2["success"], "user_id, token, list_id, item_id cannot be null")
        self.assertFalse(result3["success"], "user_id, token, list_id, item_id cannot be incorrect")
        self.assertTrue(result4["success"], "delete_item should delete successfully")

    def test_delete_shopping(self):
        result1 = shopping.delete_shoppinglist(None, None, None)
        result2 = shopping.delete_shoppinglist("", "", "")
        result3 = shopping.delete_shoppinglist("user_id", "token", "list_id")
        result4 = shopping.delete_shoppinglist(self.user_id, self.auth_token, self.list["list_id"])
        self.assertFalse(result1["success"], "user_id, token and list_id cannot be null")
        self.assertFalse(result2["success"], "user_id, token and list_id cannot be empty strings")
        self.assertFalse(result3["success"], "user_id, token and list_id cannot be incorrect")
        self.assertTrue(result4["success"], "delete list should be successful")


if __name__ == '__main__':
    unittest.main()
