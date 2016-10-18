#!/usr/bin/env python

import json


def json_account(account):
    return json.dumps(_account_to_dict(account))


def json_accounts(accounts):
    return json.dumps([_account_to_dict(a) for a in accounts])


def _account_to_dict(account):
    return {
        "id": account.key.urlsafe(),
        "max_allowed_rooms": account.max_allowed_rooms
    }


def json_chatroom(chatroom):
    return json.dumps(_chatroom_to_dict(chatroom))


def json_chatrooms(chatrooms):
    return json.dumps([_chatroom_to_dict(r) for r in chatrooms])


def _chatroom_to_dict(chatroom):
    return {
        "id": chatroom.key.urlsafe(),
        "account_id": chatroom.account_key.urlsafe(),
        "name": chatroom.name
    }


def json_users(users):
    return json.dumps([_user_to_dict(u) for u in users])


def _user_to_dict(user):
    return {
        "email": user
    }


def json_post(post):
    return json.dumps(_post_to_dict(post))


def json_posts(posts):
    return json.dumps([_post_to_dict(p) for p in posts])


def _post_to_dict(post):
    return {
        "date": post.date.isoformat(),
        "user_email": post.user_email,
        "content": post.content,
    }


def get_json_value(json_string, key_name):
    try:
        json_dict = json.loads(json_string)
        return json_dict[key_name]
    except (ValueError, KeyError):
        return None
