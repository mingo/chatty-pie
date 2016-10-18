import os
import urllib

import jinja2
import webapp2
from google.appengine.api import users

from services import get_all_accounts, get_chatrooms_in, get_posts_in

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class RedirectToAccounts(webapp2.RequestHandler):
    def get(self):
        self.redirect("/accounts/list")


class AllAccounts(webapp2.RequestHandler):
    def get(self):
        all_accounts = get_all_accounts()

        template_values = {
            "accounts": all_accounts
        }

        template = JINJA_ENVIRONMENT.get_template('templates/all-accounts.html')
        self.response.write(template.render(template_values))


class SingleAccount(webapp2.RequestHandler):
    def get(self):
        account_id = self.request.get('id')
        chatrooms = get_chatrooms_in(account_id)

        template_values = {
            "account_id": account_id,
            "chatrooms": chatrooms
        }

        template = JINJA_ENVIRONMENT.get_template('templates/single-account.html')
        self.response.write(template.render(template_values))


class SingleRoom(webapp2.RequestHandler):
    def get(self):
        room_id = self.request.get('id')
        posts = get_posts_in(room_id)

        template_values = {
            "room_id": room_id,
            "posts": posts
        }

        template = JINJA_ENVIRONMENT.get_template('templates/single-room.html')
        self.response.write(template.render(template_values))


class SignGuestbookViaForm(webapp2.RequestHandler):
    def post(self):
        # guestbook_name = get_guestbook_name_or_default(self.request.get('guestbook_name'))
        # account_id = get_account_id_or_default(self.request.get('account_id'))
        guestbook = None  # get_or_create_book(account_id, guestbook_name)

        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to ~1/second.
        greeting = None  # Greeting(parent=guestbook.key)

        if users.get_current_user():
            greeting.author = None  # Author(
            # parent=guestbook.key,
            # identity=users.get_current_user().user_id(),
            # email=users.get_current_user().email())

        # greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook.name}
        self.redirect('/?' + urllib.urlencode(query_params))
