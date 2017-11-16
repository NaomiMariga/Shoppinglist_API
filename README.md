
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
- Create shoppinglist
- View shoppinglists
- Edit shopping List
- Delete shoppinglist

> ###### Version 3 features
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

> #### Instructions to test the API locally
 - install postgreSQL
  ```sh
  apt-get install postgresql-9.6
  ```
 - install postgresql client
  ```sh
    apt install postgresql-client-9.6
  ```
  - from the commandline switch psql
  - create a user named shoppinglist with the   password "Andela100" and  a database named shoppinglist
  ```sql
  CREATE USER shoppinglist PASSWORD 'Andela100';
  CREATE DATABASE shoppinglist;
  \q -- Exit the database
  ```
 - clone the repo
 ```sh
 git clone https://github.com/NaomiMariga/Shoppinglist_API.git Shoppinglist_API
 cd Shoppinglist_API
 git checkout version_3
 ``` 
 - run the following command while inside the project directory
```sh 
  psql -d shoppinglist -U shoppinglist -W -f shoppinglist.sql
```
 -  install virtual environment system wide
 ```sh
 apt install python3.6 venv
 ```
 - make a directory for the virtual environment inside the local project folder
 ```sh
 python3.6 -m venv venv
 ```
 - activate the virtual environment
 ```sh 
 . venv/bin/activate
 ```
 - install the requirements
 ```sh
 pip install -r requirements.txt 
 ```
the following  command will run the application
```sh
python server.py
```
> ###### testing with postman
- use the API endpoints when testing with postman