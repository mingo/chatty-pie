#!/usr/bin/env python

from google.appengine.ext import ndb

from entities_validators import chatroom_type_validator


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
    users_with_access = ndb.StructuredProperty(ChatroomUser, repeated=True)


class Post(ndb.Model):
    """A main model for representing a post."""
    chatroom_key = ndb.KeyProperty(indexed=True, kind=Chatroom)
    date = ndb.DateTimeProperty(auto_now_add=True)
    user_email = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
