#!/usr/bin/env python


class IllegalChatroomTypeException(Exception):
    pass


def chatroom_type_validator(prop, value):
    if value != "standard" and value != "trial":
        raise IllegalChatroomTypeException
