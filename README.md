# Guestbook
Very simple python app that runs on Google App Engine.
This is a fork of [Google's own appengine-guestbook-python][1].

The idea is to offer a very simple application offering a REST api to guestbooks.
The [guestbook-connector][2] is using that API.

## Entities
* `Guestbook`: contains a bunch of `greetings` posted by `authors`. Has a name.
* `Greeting`: posted on a `guestbook` by an `author`. Has content and a timestamp.
* `Author`: the one posting `greetings` to `guestbooks`. Has an id and email.

## Endpoints
Here are the interesting REST endpoints:

### GET /books
````
curl localhost:8080/books
````
````
[
  {"name": "another"},
  {"name": "another book"},
  {"name": "default_guestbook"}
]
````

### POST /books
````
curl -X POST --data '{"name": "my-new-book"}' localhost:8080/books -i
````
````
HTTP/1.1 201 Created
...
````

## Requirements
* Python 2.7 - `brew install python`
* [Google Cloud SDK][3] - install it & run `gcloud init`

## How to run locally?
* `dev_appserver.py .`
* open `http://localhost:8080`

## How to deploy?
* `gcloud app deploy app.yaml index.yaml`
* Stack traces about `NeedIndexError` are transient: they will disappear after 5 minutes or so (until indices are created.)

## How to test?
TODO!

## License
This is under the Apache license.

[1]: https://github.com/GoogleCloudPlatform/appengine-guestbook-python
[2]: https://github.com/AppDirect/guestbook-connector
[3]: https://cloud.google.com/sdk/docs/
