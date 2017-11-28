import json
import os

from flask import Flask, request, Response
from flasgger import Swagger

from models.shoppinglist import Shoppinglist
from models.user import User

user = User()
shopping = Shoppinglist()

app = Flask(__name__)
Swagger(app, template_file="documentation.yml")


def dict_to_json(dct):
    return json.dumps(dct, indent=4, separators=(',', ': '))


data_sent = None


@app.before_request
def before():
    global data_sent
    if request.headers.get('Content-Type') == "application/json":
        data_sent = request.json
    else:
        print(request.headers.get('Content_Type'))
        print(request.data)
        data_sent = request.form

@app.route('/')
def welcome():
    out = {
        "message": "Welcome to shoppingList API!",
        "instructions": "use the routes below",
        "routes": {
            "register": "/auth/register",
            "login": "/auth/login",
            "reset_password": "/auth/reset-password",
            "logout": "/auth/logout",
            "change_password": "/auth/change-password"
            },
        "success": False
    }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/auth/register', methods=['POST', 'GET'])
def register():
    try:
        if request.method == 'POST':
            email = data_sent.get('email')
            username = data_sent.get('username')
            password = data_sent.get('pword')

            out = user.user_registration(email, username, password)
        else:
            out = {
                "message": "Use post to provide the below parameters",
                "parameters": "email, username and password",
                "success": False
            }
    except Exception as error:
        out = {
            "success": False,
            "message": "An exception error occurred" + str(error)
        }

    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/auth/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == 'POST':
            email = data_sent.get('email')
            password = data_sent.get('pword')
            out = user.user_login(
                email=email,
                password=password
            )
        else:
            out = {
                "message": "use POST to provide below parameters",
                "parameters": "email and password",
                "success": False
            }
    except Exception as error:
        out = {
            "success": False,
            "message": "An exception error occurred" + str(error)
            }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/auth/reset-password', methods=['POST', 'GET'])
def reset_password():
    try:
        if request.method == 'POST':
            email = data_sent.get('email')
            out = user.reset_password(email=email)
        else:
            out = {
                "success": False,
                "message": "use POST to provide below parameters",
                "parameters": "email"
            }
    except Exception as error:
        out = {
            "success": False,
            "message": "An exception error occurred" + str(error)
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/auth/logout', methods=['POST', 'GET'])
def logout():
    try:
        if request.method == 'POST':
            user_id = data_sent.get('user_id')
            token = data_sent.get('token')
            out = user.log_out(user_id=user_id, token=token)
        else:
            out = {
                "success": False,
                "message": "Use POST to provide below parameters",
                "parameters": "user_id, token"
            }
    except Exception as error:
        out = "An  exception error occurred" + str(error)
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/auth/change-password', methods=['POST', 'GET'])
def change_password():
    try:
        if request.method == 'POST':
            user_id = data_sent.get('user_id')
            token = data_sent.get('token')
            old_password = data_sent.get('old_password')
            new_password = data_sent.get('new_password')
            out = user.change_password(
                user_id=user_id,
                token=token,
                old_password=old_password,
                new_password=new_password
                )
        else:
            out = {
                "success": False,
                "message": "use POST to provide below parameters ",
                "parameters": "user_id, token, old_password, new_password"
            }
    except Exception as error:
        out = {
            "message": "An exception error occurred" + str(error),
            "success": False
            }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/shoppinglists', methods=['POST', 'GET'])
def shoppinglist_create_and_view():
    try:
        if request.method == 'POST':
            user_id = data_sent.get('user_id')
            token = data_sent.get('token')
            list_name = data_sent.get('list_name')

            out = shopping.create_shoppinglist(user_id, token, list_name)

        elif request.method == 'GET':
            user_id = request.args.get('user_id')
            token = request.args.get('token')

            out = shopping.read_shoppinglist(user_id, token)

        else:
            out = {
                "success": False,
                "message": "use POST or GET to provide below parameters",
                "parameters for POST": "user_id, token, list_name",
                "parameters for GET": "user_id, token"
            }
    except Exception as error:
        out = {
            "message": "An exception error occurred in server" + str(error),
            "success": False
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/shoppinglists/<int:list_id>', methods=['PUT', 'GET', 'DELETE'])
def shoppinglist(list_id):
    try:
        if request.method == 'PUT':
            user_id = data_sent.get('user_id')
            token = data_sent.get('token')
            list_name = data_sent.get('list_name')
            out = shopping.edit_shoppinglist(list_id=list_id, user_id=user_id, token=token, list_name=list_name)
        elif request.method == 'DELETE':
            user_id = data_sent.get('user_id')
            token = data_sent.get('token')
            out = shopping.delete_shoppinglist(user_id, token, list_id)
        elif request.method == 'GET':
            user_id = request.args.get('user_id')
            token = request.args.get('token')
            page = str(request.args.get('page', "1"))
            count = str(request.args.get('count', "10"))
            search = request.args.get('q', "")
            if not page.isnumeric():
                page = 1
            page = int(page)
            if not count.isnumeric():
                count = 10
            count = int(count)
            offset = (page - 1) * count

            out = shopping.read_items(user_id, token, list_id, count, offset, search)
        else:
            out = {
                "success": False,
                "message": "use PUT, DELETE or POST to provide below parameters",
                "parameters": "user_id, token",
                "optional parameters": "page, count"
            }
    except Exception as error:
        out = {
            "success": False,
            "message": "An exception error occurred " + str(error)
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/shoppinglists/<int:list_id>/items', methods=['POST'])
def add_items(list_id):
    try:
        if request.method == 'POST':
            user_id = data_sent.get('user_id')
            token = data_sent.get('token')
            item_name = data_sent.get('item_name')
            quantity = data_sent.get('quantity')
            units = data_sent.get('units')
            cost = data_sent.get('cost')
            out = shopping.add_items(user_id, token, list_id, item_name, quantity, units,cost)
        else:
            out = {
                "success": False,
                "message": "Use POST to provide the below parameters",
                "parameters": "user_id, token, item_name, quantity, units, cost"
            }
    except Exception as error:
        out = {
            "success": False,
            "message": "An exception error occurred" + str(error)
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/shoppinglists/<int:list_id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
def edit_and_delete_items(list_id, item_id):
    try:
        if request.method == 'PUT':
            user_id = data_sent.get('user_id')
            token = data_sent.get('token')
            attribute = data_sent.get('attribute')
            value = data_sent.get('value')
            out = shopping.edit_items(user_id, token, list_id, item_id, attribute, value)
        elif request.method == 'DELETE':
            user_id = data_sent.get('user_id')
            token = data_sent.get('token')
            out = shopping.delete_items(user_id, token, list_id, item_id)
        else:
            out = {
                "success": False,
                "message": "use POST or DELETE to provide parameters as shown below",
                "parameters for PUT": "user_id, token, attribute(list_name, quantity, units, quantity), value",
                "parameters for DELETE": "user_id, token"
            }
    except Exception as error:
        out = {
            "success": False,
            "message": "An exception error occurred" + str(error)
        }
    return Response(dict_to_json(out), mimetype="text/json")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
