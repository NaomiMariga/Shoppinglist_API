

#### Shoppinglist_API is a Persistent Flask API version of the Shoppinglist application that allows users to keep track of the items they wish to purchase while maintaining budget.
#### Versions
- version 1
- version 2
- version 3

> ###### Version 1 features
- User registration
- User login
- Reset Password
- Change Password
- Logout
-
> ###### Version 2 features
- User registration
- User login
- Reset Password
- Change Password
- Logout
- Create shoppinglist
- View shoppinglists
- Edit shoppinglist
- Delete shoppinglist

> ###### Version 3 features
- User registration
- User login
- Reset Password
- Change Password
- Logout
- Create shoppinglist
- View shoppinglists
- Edit shopping List
- Delete shoppinglist
- Add shoppinglist items
- view shopping list items
- Edit shoppinglist items
- Delete shoppinglist items

> #### Endpoints for the API
> default root for the API
      - host 0.0.0.0
      - port 5000
      - http://0.0.0.0:5000

|Function|Method|Route|
|--------|------|-----|
|Registration |POST  |/auth/register|
|Login    |POST  |/auth/login|
|Reset password|POST  |/auth/reset-password|
|Change password|POST |/auth/change-password|
|Logout|POST |/auth/logout|
|Create shoppinglist|POST|/shoppinglists|
|View shoppinglist|GET|/shoppinglists|
|Edit shoppinglist|PUT|/shoppinglists/<list_id>|
|Delete shoppinglist|DELETE|/shoppinglists/<list_id>|
|Add shoppinglist items|POST|/shoppinglists/<list_id>/items|
|view shoppinglist items|GET|/shoppinglists/<list_id>|
|Edit shoppinglist items|PUT|/shoppinglists/<list_id>/items/<item_id>
|Delete shoppinglist items|DELETE|/shoppinglists/<list_id>/items/<item_id>|
