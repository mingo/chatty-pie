import os
import urllib

import jinja2
import webapp2
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class UnderConstruction(webapp2.RequestHandler):
    def get(self):
        self.response.write("<html><body>Under construction! Nothing to see now.</body></html>")


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


class RenderGuestbook(webapp2.RequestHandler):
    def get(self):
        guestbook_name = "default_guestbook"  # get_guestbook_name_or_default(self.request.get('guestbook_name'))
        greetings = []  # get_all_greetings_in_book(guestbook_name)

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

        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))
