
#### Shoppinglist_API is a Persistent Flask API version of the Shoppinglist application that allows users to keep track of the items they wish to purchase while maintaining budget.
[![Build Status](https://travis-ci.org/NaomiMariga/Shoppinglist_API.svg?branch=version_3)](https://travis-ci.org/NaomiMariga/Shoppinglist_API)
[![Coverage Status](https://coveralls.io/repos/github/NaomiMariga/Shoppinglist_API/badge.svg?branch=version_3)](https://coveralls.io/github/NaomiMariga/Shoppinglist_API?branch=version_3)

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
 - now to create tables in the database
 ```sh
 alembic upgrade head
 ```
the following  command will run the application
```sh
python server.py
```
> ###### testing with postman
- use the API endpoints when testing with postman

> #### instructions to testing the API manually

- use the below link to test the API with postman using the endpoints given earlier
[https://naomishoppinglist-api.herokuapp.com](https://naomishoppinglist-api.herokuapp.com)

- use the link below to view the documentation
[Shoppinglist API Documentation](https://naomishoppinglist-api.herokuapp.com/apidocs)