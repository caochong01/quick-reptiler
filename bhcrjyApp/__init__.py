# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template

from bhcrjyApp import blueprint_url
from bhcrjyApp.redisConfig import redis_db

app = Flask(__name__, instance_relative_config=True)


def create_app(app_config=None):
    """
    Create and configure an instance of the Flask application.
    :param app_config:
    :return:
    """

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY=b'\xdd\xe7\x8c\xd6m\xe4O\x150m\xc4w\x8f\xe2\xa1\xbc',
        # store the database in the instance folder
        # DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if app_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("settings.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(app_config)

    @app.route("/test")
    def test():
        return "Hello, World!"

    @app.errorhandler(404)
    def not_found(error):
        app.logger.debug(error)
        return render_template('error/error404.html'), 404

    # register the database commands

    # apply the blueprints to the app
    blueprint_url.app_register(app)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    # register the redis commands
    redis_db.init_app(app)

    return app


if __name__ == '__main__':
    create_app().run(debug=True, port=8282)
