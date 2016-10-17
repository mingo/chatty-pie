#!/usr/bin/env python

from services import get_account_id_or_default, get_account, create_account


def create_default_account_if_needed():
    default_account_id = get_account_id_or_default("")
    try:
        get_account(default_account_id)
    except LookupError:
        create_account(100, default_account_id)
