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

from google.appengine.ext import ndb

from entities_validators import chatroom_type_validator, chatroom_status_validator


class Account(ndb.Model):
    """A main model for representing an account, owning chatrooms."""
    max_allowed_rooms = ndb.IntegerProperty(indexed=False)


class ChatroomUser(ndb.Model):
    """A sub model for representing a user in a chatroom."""
    email = ndb.StringProperty(indexed=False)
    can_see_all_history = ndb.BooleanProperty(indexed=False)


class Chatroom(ndb.Model):
    """A main model for representing a chatroom."""
    account_key = ndb.KeyProperty(indexed=True, kind=Account)
    name = ndb.StringProperty(indexed=False)
    type = ndb.StringProperty(indexed=False, validator=chatroom_type_validator)
    status = ndb.StringProperty(indexed=False, validator=chatroom_status_validator)
    users_with_access = ndb.StructuredProperty(ChatroomUser, repeated=True)
    full_history_enabled = ndb.BooleanProperty()


class Post(ndb.Model):
    """A main model for representing a post."""
    chatroom_key = ndb.KeyProperty(indexed=True, kind=Chatroom)
    date = ndb.DateTimeProperty(auto_now_add=True)
    user_email = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
