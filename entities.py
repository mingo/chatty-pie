#!/usr/bin/env python

from google.appengine.ext import ndb


class Account(ndb.Model):
    """A main model for representing an account, owning chatrooms."""
    max_allowed_rooms = ndb.IntegerProperty(indexed=False)


class Chatroom(ndb.Model):
    """A main model for representing a chatroom."""
    account_key = ndb.KeyProperty(indexed=True, kind=Account)
    name = ndb.StringProperty(indexed=False)
    users_with_access = ndb.StringProperty(indexed=False, repeated=True)


class Post(ndb.Model):
    """A main model for representing a post."""
    chatroom_key = ndb.KeyProperty(indexed=True, kind=Chatroom)
    date = ndb.DateTimeProperty(auto_now_add=True)
    user_email = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
