import pymysql
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host=current_app.config['MYSQL_DATABASE_HOST'],
            user=current_app.config['MYSQL_DATABASE_USER'],
            password=current_app.config['MYSQL_DATABASE_PASSWORD'],
            db=current_app.config['MYSQL_DATABASE_DB'],
            charset=current_app.config['MYSQL_DATABASE_CHARSET'],
            cursorclass=pymysql.cursors.DictCursor
        )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db = get_db()
        db.close()
