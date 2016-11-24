import os

import jinja2
import webapp2

from services import get_all_accounts, get_chatrooms_in, get_posts_in, get_chatroom, get_all_chatrooms, \
    get_all_users_allowed_in

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

        template = JINJA_ENVIRONMENT.get_template('templates/account-all.html')
        self.response.write(template.render(template_values))


class SingleAccount(webapp2.RequestHandler):
    def get(self):
        account_id = self.request.get('id')
        chatrooms = get_chatrooms_in(account_id)

        template_values = {
            "account_id": account_id,
            "chatrooms": chatrooms
        }

        template = JINJA_ENVIRONMENT.get_template('templates/account-single.html')
        self.response.write(template.render(template_values))


class AllRooms(webapp2.RequestHandler):
    def get(self):
        all_rooms = get_all_chatrooms()

        template_values = {
            "chatrooms": all_rooms
        }

        template = JINJA_ENVIRONMENT.get_template('templates/room-all.html')
        self.response.write(template.render(template_values))


class SingleRoom(webapp2.RequestHandler):
    def get(self):
        room_id = self.request.get('id')
        room = get_chatroom(room_id)
        posts = get_posts_in(room_id)
        users = get_all_users_allowed_in(room_id)

        template_values = {
            "room_name": room.name,
            "room_id": room_id,
            "room_status": room.status,
            "room_type": room.type,
            "posts": posts,
            "users": users
        }

        template = JINJA_ENVIRONMENT.get_template('templates/room-single.html')
        self.response.write(template.render(template_values))
