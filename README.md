# Guestbook
Very simple python app that runs on Google App Engine.
This is a fork of [Google's own appengine-guestbook-python][1].

The idea is to offer a very simple application offering a REST api to guestbooks.
The [guestbook-connector][2] is using that API.

## Requirements
* Python 2.7 - `brew install python`
* [Google Cloud SDK][3] - install it & run `gcloud init`

## How to run locally?
`dev_appserver.py .`

## How to deploy?
* `gcloud app deploy`
* Stack traces about `NeedIndexError` are transient: they will disappear after 5 minutes or so (until indices are created.)

## How to test?
TODO!

## License
This is under the Apache license.

[1]: https://github.com/GoogleCloudPlatform/appengine-guestbook-python
[2]: https://github.com/AppDirect/guestbook-connector
[3]: https://cloud.google.com/sdk/docs/
