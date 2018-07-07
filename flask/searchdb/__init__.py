import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        MYSQL_DATABASE_USER = 'tomoro',
        MYSQL_DATABASE_PASSWORD = 'tomo',
        MYSQL_DATABASE_DB = 'patent',
        MYSQL_DATABASE_HOST = 'localhost',
        #MYSQL_DATABASE_HOST = '192.168.2.107',
        MYSQL_DATABASE_CHARSET = 'utf8',
        JSON_AS_ASCII = False
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import search
    app.register_blueprint(search.bp)
    app.add_url_rule('/search', endpoint='search')


    return app
