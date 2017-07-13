# chatty-pie
![a chatty magpie](http://i.imgur.com/Wj2wJev.jpg)

Simple application offering a REST api to buy chat rooms for their users.
The [chatty-pie-connector][1] is using that API.

This is a Python app that runs on Google App Engine.
This started as a fork of [Google's own appengine-guestbook-python][2].
So thank Google for the original code.

Master is deployed on 2 environments:
* dev: https://operating-attic-146121.appspot.com/
* prod: https://chattypie-148413.appspot.com/

## Entities
* `Account`: it owns a bunch of `chatrooms`.
* `Chatroom`: contains a bunch of `posts` made by `users`. Has a name, a type (`trial` or `standard`), a status (`active` or `suspended`) and is owned by an `Account`.
* `Post`: added to a `chatroom` by a `user`. Has content and a timestamp.
* `User`: the one making `posts` to `chatrooms`. Can have access to >1 rooms.

## Endpoints
* GET /accounts - lists all accounts
````
curl localhost:8080/accounts
````
````
[
  {"id": "aghkZXZ-Tm9uZXIUCxIH",  "max_allowed_rooms": 200},
  ...
]
````

* POST /accounts - creates a new account
````
curl -X POST --data '{"max_allowed_rooms": 100}' localhost:8080/accounts -i
````
````
HTTP/1.1 201 Created
...
{
  "max_allowed_rooms": 100,
  "id": "aghkZXZ-TuZDFUCxIHER5"
}
````

* GET /accounts/[ACCOUNT_ID]/rooms - lists all rooms in a given account
````
curl localhost:8080/accounts/aghkZXZ-TuZDFUCxIHER5/rooms
````
````
[
  {
    "account_id": "aghkZXZ-TuZDFUCxIHER5",
    "id": "aghkZXZ-Tm9uZXIVCxIIQ2hhdHJvb20YgICAgIDyiAkM",
    "name": "my first room",
    "type": "standard",
    "status": "active"
  },
  ...
]
````

* GET /accounts/[ACCOUNT_ID]/domains/[DOMAIN_NAME]/ownershipRecords - Shows the ownership verification token for that account and domain
````
curl localhost:8080/accounts/aghkZXZ-TuZDFUCxIHER5/domains/example.com/ownershipRecords
````
````
  {
    "account": "aghkZXZ-TuZDFUCxIHER5", 
    "domain": "example.com",
    "token": "chatty-pie-verification=agdffhdhkZXZ-TuZDFUCxIHER5FGGFsdfgs",
    "record_type": "TXT"
  }
````

* POST /accounts/[ACCOUNT_ID]/domains/[DOMAIN_NAME]/triggerOwnershipVerification - signals chatty pie that it can begin the ownership verification process
````
curl -X POST localhost:8080/accounts/aghkZXZ-TuZDFUCxIHER5/domains/example.com/triggerOwnershipVerification
````
````
HTTP/1.1 200 OK
````
Note that this API will return 400 if the account does not exist, or if the validation proof has never been requested for
that account and domain name combination

* GET /rooms - lists all rooms across all accounts
````
curl localhost:8080/rooms
````
````
[
  {
    "account_id": "aghkZXZ-TuZDFUCxIHER5",
    "id": "aghkZXZ-Tm9uZXIVCxIIQ2hhdHJvb20YgICAgIDyiAkM",
    "name": "my first room",
    "type": "standard",
    "status": "active"
  },
  ...
]
````

* POST /accounts/[ACCOUNT_ID]/rooms - creates a new room in a given account
````
curl -X POST --data '{"name": "my new corporate room"}' localhost:8080/accounts/aghkZXZ-TuZDFUCxIHER5/rooms -i
````
````
HTTP/1.1 201 Created
...
{
  "account_id": "aghkZXZ-TuZDFUCxIHER5",
  "id": "aghkZXZ-Tm9uZXIVCxVVV",
  "name": "my new corporate room",
  "type": "standard",
  "status": "active"
}
````

* PUT /rooms/[ROOM_ID] - updates the status, type or access to full history for an existing room
````
curl -X PUT --data '{"type": "trial", "status": "suspended", "full_history_enabled": true}' localhost:8080/rooms/aghkZXZ-Tm9uZXIVCxVVV -i
````
````
HTTP/1.1 204 No Content
...
````

* GET /rooms/[ROOM_ID]/users - lists users which have access to a given room
````
curl localhost:8080/rooms/aghkZXZ-Tm9uZXIVCxVVV/users
````
````
[
  {
    "email": "someuser@some.com"
  },
  ...
]
````

* POST /rooms/[ROOM_ID]/users/[USER_EMAIL] - grants access to a user for a given room
````
curl -X POST --data '' localhost:8080/rooms/aghkZXZ-Tm9uZXIVCxVVV/users/auser@example.com -i
````
````
HTTP/1.1 204 No Content
...
````

* DELETE /rooms/[ROOM_ID]/users/[USER_EMAIL] - grants access to a user for a given room
````
curl -X DELETE localhost:8080/rooms/aghkZXZ-Tm9uZXIVCxVVV/users/auser@example.com -i
````
````
HTTP/1.1 204 No Content
...
````

* GET /rooms/[ROOM_ID]/posts - lists all posts in a given room
````
curl localhost:8080/rooms/aghkZXZ-Tm9uZXIVCxVVV/posts
````
````
[
  {
    "user_email": "user@email.com",
    "content": "This is my first post <br>",
    "date": "2016-10-17T20:43:39.367700"
  },
  ...
]
````

* POST /rooms/[ROOM_ID]/posts - adds a posts to a given room; user must be allowed to.
````
curl -X POST --data '{"user_email": "user@email.com", "content": "This is my first post <br>"}' localhost:8080/rooms/aghkZXZ-Tm9uZXIVCxVVV/posts -i
````
````
HTTP/1.1 201 Created
...
{
    "content": "This is my first post <br>",
    "date": "2016-10-17T20:43:39.367700",
    "user_email": "user@email.com"
}
````

* DELETE /rooms/[ROOM_ID] - delete a room by id
````
curl -X DELETE localhost:8080/rooms/aghkZXZ-Tm9uZXIVCxIIQ2hhdHJvb20YgICAgIDQuwsM -i
````
````
HTTP/1.1 200 OK
content-type: application/json; charset=utf-8
cache-control: no-cache
Content-Length: 32
Server: Development/2.0
Date: Thu, 03 Nov 2016 14:31:22 GMT

{
    "message": "Delete successful"
}
````

## Requirements
* Python 2.7 - `brew install python`
* [Google Cloud SDK][3] - install it & run `gcloud init`

## How to develop?
* use [pycharm][4] or any text editor

## How to run locally?
* have the requirements: `python` & `gcloud`.
* `dev_appserver.py .`
* open `http://localhost:8080`

## How to deploy?
* `gcloud app deploy app.yaml`
* Stack traces about `NeedIndexError` are transient: they will disappear after 5 minutes or so (until indices are created.)

## How to test?
* chatty-pie's purchase and cancel flows are automate and can be run using E2E portal
  * Navigate to https://e2e.appdirect.com and login
  * Click on trigger run 
  * Select your Appdirect PR from drop down
  * Test Suite: pi/products/chattypie/chatty_pie

## License
Most of the code is Copyright 2016 Google Inc.
Everything is under the Apache license.

[1]: https://github.com/AppDirect/chatty-pie-connector
[2]: https://github.com/GoogleCloudPlatform/appengine-guestbook-python
[3]: https://cloud.google.com/sdk/docs/
[4]: https://www.jetbrains.com/pycharm/nextversion/
