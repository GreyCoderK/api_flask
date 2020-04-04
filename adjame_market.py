import os
from os.path import join, dirname

from app import create_app, db
from app.models import User, Article, MenuVertical, TypeArticle, TypeUser
from dotenv import load_dotenv

env_path = join(dirname(dirname(__file__)),'.flaskenv')
load_dotenv(env_path)

config_name = os.environ.get('FLASK_ENV')

app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'TypeUser': TypeUser,
        'TypeArticle': TypeArticle,
        'Article': Article,
        'MenuVertical': MenuVertical 
    }