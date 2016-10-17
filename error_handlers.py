#!/usr/bin/env python


def handle_400(request, response, exception):
    response.write(exception)
    response.set_status(400)
    return
