import json
import os

from flask import Flask, request, Response

from user import User
from shoppinglist import Shoppinglist

user = User()
shopping = Shoppinglist()

app = Flask(__name__)


def dict_to_json(dct):
    return json.dumps(dct, indent=4, separators=(',', ': '))


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
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('pword')

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
            email = request.form.get('email')
            password = request.form.get('pword')
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
            email = request.form.get('email')
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
            user_id = request.form.get('user_id')
            token = request.form.get('token')
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
            user_id = request.form.get('user_id')
            token = request.form.get('token')
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
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
            user_id = request.form.get('user_id')
            token = request.form.get('token')
            list_name = request.form.get('list_name')

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
            user_id = request.form.get('user_id')
            token = request.form.get('token')
            list_name = request.form.get('list_name')
            out = shopping.edit_shoppinglist(list_id=list_id, user_id=user_id, token=token, list_name=list_name)
        elif request.method == 'DELETE':
            user_id = request.form.get('user_id')
            token = request.form.get('token')
            out = shopping.delete_shoppinglist(user_id, token, list_id)
        elif request.method == 'GET':
            user_id = request.args.get('user_id')
            token = request.args.get('token')
            out = shopping.read_items(user_id, token, list_id)
        else:
            out = {
                "success": False,
                "message": "use PUT, DELETE or POST to provide below parameters",
                "parameters": "user_id, token"
            }
    except Exception as error:
        out = {
            "success": False,
            "message": "An exception error occurred " + str(error)
        }
    return Response(dict_to_json(out), mimetype="text/json")


@app.route('/shoppinglists/<int:list_id>/items/', methods=['POST'])
def add_items(list_id):
    try:
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            token = request.form.get('token')
            item_name = request.form.get('item_name')
            quantity = request.form.get('quantity')
            units = request.form.get('units')
            cost = request.form.get('cost')
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
            user_id = request.form.get('user_id')
            token = request.form.get('token')
            attribute = request.form.get('attribute')
            value = request.form.get('value')
            out = shopping.edit_items(user_id, token, list_id, item_id, attribute, value)
        elif request.method == 'DELETE':
            user_id = request.form.get('user_id')
            token = request.form.get('token')
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
