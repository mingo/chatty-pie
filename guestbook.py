#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import urllib

import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


def get_or_create_book(guestbook_name):
    guestbook = ndb.Key(Guestbook, guestbook_name).get()
    if guestbook is None:
        guestbook = Guestbook(id=guestbook_name, name=guestbook_name)
        guestbook.put()
    return guestbook


def get_all_books():
    return Guestbook.query().fetch()


def get_all_greetings_in_book(guestbook_name):
    guestbook_key = ndb.Key(Guestbook, guestbook_name)
    return Greeting.query(ancestor=guestbook_key) \
        .order(-Greeting.date) \
        .fetch(20)


class Guestbook(ndb.Model):
    """A main model for representing a guestbook."""
    name = ndb.StringProperty(indexed=False)


class Author(ndb.Model):
    """Sub model for representing an author, in a guestbook."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class RenderGuestbookHtml(webapp2.RequestHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greetings = get_all_greetings_in_book(guestbook_name)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class SignGuestbookViaForm(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        guestbook = get_or_create_book(guestbook_name)

        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to ~1/second.
        greeting = Greeting(parent=guestbook.key)

        if users.get_current_user():
            greeting.author = Author(
                parent=guestbook.key,
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook.name}
        self.redirect('/?' + urllib.urlencode(query_params))


class ListGuestbooks(webapp2.RequestHandler):
    def get(self):
        allBooks = get_all_books()
        self.response.content_type = "application/json"
        self.response.write(json.dumps([b.to_dict() for b in allBooks]))


app = webapp2.WSGIApplication([
    ('/', RenderGuestbookHtml),
    ('/sign', SignGuestbookViaForm),
    ('/books', ListGuestbooks),
], debug=True)
