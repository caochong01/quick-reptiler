# -*- coding: utf-8 -*-
from bhcrjyApp.app import login, index, looktax, user


# Add your module and introduce it into the blueprint
# Initialization of blueprint needs to be introduced into app
def app_register_blueprint(app):
    app.register_blueprint(login.bp)
    app.register_blueprint(index.bp)
    app.register_blueprint(looktax.bp)
    app.register_blueprint(user.bp)
    return app


app_register = app_register_blueprint
