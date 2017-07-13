#!/usr/bin/env python

# Copyright 2017 AppDirect, Inc. and/or its affiliates
# Copyright 2016 Google Inc
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json


def json_domain_ownership_proof(domain_ownership_proof):
    return json.dumps(_ownership_proof_to_dict(domain_ownership_proof))


def json_account(account):
    return json.dumps(_account_to_dict(account))


def json_accounts(accounts):
    return json.dumps([_account_to_dict(a) for a in accounts])


def _account_to_dict(account):
    return {
        "id": account.key.urlsafe(),
        "max_allowed_rooms": account.max_allowed_rooms
    }


def _ownership_proof_to_dict(domain_ownership_proof):
    return {
        "account": domain_ownership_proof.account_id,
        "token": "chatty-pie-verification=" + domain_ownership_proof.key.urlsafe(),
        "domain": domain_ownership_proof.domain_name,
        "record_type": "TXT"
    }


def json_chatroom(chatroom):
    return json.dumps(_chatroom_to_dict(chatroom))


def json_chatrooms(chatrooms):
    return json.dumps([_chatroom_to_dict(r) for r in chatrooms])


def _chatroom_to_dict(chatroom):
    return {
        "id": chatroom.key.urlsafe(),
        "account_id": chatroom.account_key.urlsafe(),
        "name": chatroom.name,
        "type": chatroom.type,
        "status": chatroom.status,
        "full_history_enabled": chatroom.full_history_enabled
    }


def json_users(users):
    return json.dumps([_user_to_dict(u) for u in users])


def _user_to_dict(user):
    return {
        "email": user.email
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
