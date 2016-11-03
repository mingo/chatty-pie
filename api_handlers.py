#!/usr/bin/env python

import webapp2

from json_helpers import json_account, get_json_value, json_accounts, json_chatroom, json_chatrooms, json_users, \
    json_posts, json_post
from services import create_account, get_all_accounts, create_chatroom, delete_chatroom, get_all_chatrooms, \
    allow_user_access_in_chatroom, \
    get_chatrooms_in, get_all_users_allowed_in, get_posts_in, create_post


class JsonApiHandler(webapp2.RequestHandler):
    def get_mandatory_json_value(self, key_name):
        value = get_json_value(self.request.body, key_name)
        if value is None:
            self.abort(400, "missing " + key_name + " param")
        return value


class AccountApi(JsonApiHandler):
    def get(self):
        all_accounts = get_all_accounts()
        write_json_response(self.response, 200, json_accounts(all_accounts))

    def post(self):
        max_allowed_rooms = self.get_mandatory_json_value("max_allowed_rooms")

        account = create_account(max_allowed_rooms)

        write_json_response(self.response, 201, json_account(account))


class ChatroomApi(JsonApiHandler):
    def get(self, account_id):
        all_chatrooms_in_this_account = get_chatrooms_in(account_id)
        write_json_response(self.response, 200, json_chatrooms(all_chatrooms_in_this_account))

    def get_all_rooms(self):
        all_chatrooms = get_all_chatrooms()
        write_json_response(self.response, 200, json_chatrooms(all_chatrooms))

    def post(self, account_id):
        chatroom_name = self.get_mandatory_json_value("name")

        chatroom = create_chatroom(account_id, chatroom_name)

        write_json_response(self.response, 201, json_chatroom(chatroom))

    def delete(self, chatroom_id):
        delete_chatroom(chatroom_id)
        write_json_response(self.response, 200, "{\"message\": \"Delete successful\"}")

class UserAccessApi(JsonApiHandler):
    def get(self, chatroom_id):
        all_users_allowed_in_chatroom = get_all_users_allowed_in(chatroom_id)
        write_json_response(self.response, 200, json_users(all_users_allowed_in_chatroom))

    def put(self, chatroom_id):
        user_email = self.get_mandatory_json_value("email")

        allow_user_access_in_chatroom(chatroom_id, user_email)

        self.response.status = 204

class PostApi(JsonApiHandler):
    def get(self, chatroom_id):
        all_posts_in_this_chatroom = get_posts_in(chatroom_id)
        write_json_response(self.response, 200, json_posts(all_posts_in_this_chatroom))

    def post(self, chatroom_id):
        user_email = self.get_mandatory_json_value("user_email")
        content = self.get_mandatory_json_value("content")

        post = create_post(chatroom_id, user_email, content)

        write_json_response(self.response, 201, json_post(post))


def write_json_response(response, status_code, json_body):
    response.content_type = "application/json"
    response.write(json_body)
    response.status = status_code
