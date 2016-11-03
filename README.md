# chatty-pie
![a chatty magpie](http://i.imgur.com/Wj2wJev.jpg)

Simple application offering a REST api to buy chat rooms for their users.
The [chatty-pie-connector][1] is using that API.

This is a Python app that runs on Google App Engine.
This started as a fork of [Google's own appengine-guestbook-python][2].
So thank Google for the original code.

Master is deployed here https://operating-attic-146121.appspot.com/

## Entities
* `Account`: it owns a bunch of `chatrooms`.
* `Chatroom`: contains a bunch of `posts` made by `users`. Has a name and is owned by an `Account`.
* `Post`: added to a `chatroom` by a `user`. Has content and a timestamp.
* `User`: the one making `posts` to `chatrooms`. For now, this is just an email. Can have access to >1 rooms.

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
    "name": "my first room"
  },
  ...
]
````

* GET /rooms - lists all rooms across all accounts
````
curl localhost:8080/rooms
````
````
[
  {
    "account_id": "aghkZXZ-TuZDFUCxIHER5",
    "id": "aghkZXZ-Tm9uZXIVCxIIQ2hhdHJvb20YgICAgIDyiAkM",
    "name": "my first room"
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
  "name": "my new corporate room"
}
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

* PUT /rooms/[ROOM_ID]/users - grants access to a user for a given room
````
curl -X PUT --data '{"email": "user@email.com"}' localhost:8080/rooms/aghkZXZ-Tm9uZXIVCxVVV/users -i
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
...
````

## Requirements
* Python 2.7 - `brew install python`
* [Google Cloud SDK][3] - install it & run `gcloud init`

## How to run locally?
* have the requirements: `python` & `gcloud`.
* `dev_appserver.py .`
* open `http://localhost:8080`

## How to deploy?
* `gcloud app deploy app.yaml`
* Stack traces about `NeedIndexError` are transient: they will disappear after 5 minutes or so (until indices are created.)

## How to test?
TODO!

## License
Most of the code is Copyright 2016 Google Inc.
Everything is under the Apache license.

[1]: https://github.com/AppDirect/chatty-pie-connector
[2]: https://github.com/GoogleCloudPlatform/appengine-guestbook-python
[3]: https://cloud.google.com/sdk/docs/
