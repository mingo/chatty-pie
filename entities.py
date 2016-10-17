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
