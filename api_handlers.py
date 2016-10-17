#!/usr/bin/env python

import webapp2

from json_helpers import json_account, get_json_value, json_accounts, json_chatroom, json_chatrooms, json_users
from services import create_account, get_all_accounts, create_chatroom, get_all_chatrooms, \
    allow_user_access_in_chatroom, \
    get_chatrooms_in, get_all_users_allowed_in


class AccountApi(webapp2.RequestHandler):
    def get(self):
        all_accounts = get_all_accounts()
        write_json_response(self.response, 200, json_accounts(all_accounts))

    def post(self):
        max_allowed_rooms = get_json_value(self.request.body, "max_allowed_rooms")
        if max_allowed_rooms is None:
            self.abort(400, "missing max_allowed_rooms integer param")

        account = create_account(max_allowed_rooms)

        write_json_response(self.response, 201, json_account(account))


class ChatroomApi(webapp2.RequestHandler):
    def get(self, account_id):
        all_chatrooms_in_this_account = get_chatrooms_in(account_id)
        write_json_response(self.response, 200, json_chatrooms(all_chatrooms_in_this_account))

    def get_all_rooms(self):
        all_chatrooms = get_all_chatrooms()
        write_json_response(self.response, 200, json_chatrooms(all_chatrooms))

    def post(self, account_id):
        chatroom_name = get_json_value(self.request.body, "name")
        if chatroom_name is None:
            self.abort(400, "missing name string param")

        chatroom = create_chatroom(account_id, chatroom_name)

        write_json_response(self.response, 201, json_chatroom(chatroom))


class UserAccessApi(webapp2.RequestHandler):
    def get(self, chatroom_id):
        all_users_allowed_in_chatroom = get_all_users_allowed_in(chatroom_id)
        write_json_response(self.response, 200, json_users(all_users_allowed_in_chatroom))

    def put(self, chatroom_id):
        user_email = get_json_value(self.request.body, "email")
        if user_email is None:
            self.abort(400, "missing email string param")

        allow_user_access_in_chatroom(chatroom_id, user_email)

        self.response.status = 204


def write_json_response(response, status_code, json_body):
    response.content_type = "application/json"
    response.write(json_body)
    response.status = status_code
