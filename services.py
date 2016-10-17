#!/usr/bin/env python

from google.appengine.ext import ndb

from entities import Account, Chatroom


def get_account(account_id):
    account = Account.get_by_id(account_id)
    if account is None:
        raise LookupError("Cannot find an account with id " + account_id)
    return account


def get_all_accounts():
    return Account.query().fetch()


def create_account(max_allowed_rooms):
    account = Account(max_allowed_rooms=max_allowed_rooms)
    account.put()

    return account


def get_all_chatrooms():
    return Chatroom.query().fetch()


def get_chatrooms_in(urlsafe_account_id):
    account_key = ndb.Key(urlsafe=urlsafe_account_id)
    return Chatroom.query(Chatroom.account_key == account_key).fetch()


def create_chatroom(urlsafe_account_id, name):
    account_key = ndb.Key(urlsafe=urlsafe_account_id)
    chatroom = Chatroom(account_key=account_key, name=name)
    chatroom.put()

    return chatroom


def get_all_users_allowed_in(urlsafe_chatroom_id):
    return ndb.Key(urlsafe=urlsafe_chatroom_id).get().users_with_access


def allow_user_access_in_chatroom(urlsafe_chatroom_id, user_email):
    chatroom = ndb.Key(urlsafe=urlsafe_chatroom_id).get()
    chatroom.users_with_access.append(user_email)

    chatroom.put()
