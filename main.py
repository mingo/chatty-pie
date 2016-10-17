#!/usr/bin/env python

import webapp2

from api_handlers import AccountApi, ChatroomApi, UserAccessApi
from error_handlers import handle_400
from html_handlers import UnderConstruction

app = webapp2.WSGIApplication([
    webapp2.Route('/', UnderConstruction),
    webapp2.Route('/accounts', AccountApi),
    webapp2.Route('/accounts/<account_id>/rooms', ChatroomApi),
    webapp2.Route('/rooms', ChatroomApi, methods=["GET"], handler_method="get_all_rooms"),
    webapp2.Route('/rooms/<chatroom_id>/users', UserAccessApi)
], debug=True)
app.error_handlers[400] = handle_400
