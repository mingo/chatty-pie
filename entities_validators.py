#!/usr/bin/env python


class IllegalChatroomTypeException(Exception):
    pass


class IllegalChatroomStatusException(Exception):
    pass


def chatroom_type_validator(prop, value):
    if value != "standard" and value != "trial":
        raise IllegalChatroomTypeException
    return value


def chatroom_status_validator(prop, value):
    if value != "active" and value != "suspended":
        raise IllegalChatroomStatusException
    return value
