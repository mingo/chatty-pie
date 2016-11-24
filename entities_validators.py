#!/usr/bin/env python


class IllegalChatroomTypeException(ValueError):
    pass


class IllegalChatroomStatusException(ValueError):
    pass


def chatroom_type_validator(prop, value):
    if value != "standard" and value != "trial":
        raise IllegalChatroomTypeException("A chatroom type must be either 'trial' or 'standard'")
    return value


def chatroom_status_validator(prop, value):
    if value != "active" and value != "suspended":
        raise IllegalChatroomStatusException("A chatroom status must be either 'active' or 'suspended'")
    return value
