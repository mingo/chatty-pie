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
