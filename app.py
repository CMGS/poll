import config
import logging
from models import init_db
from flask import Flask, redirect

from dae.api.users import get_current_user, create_login_url

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.config.update(
    SQLALCHEMY_DATABASE_URI = config.DATABASE_URI,
    SQLALCHEMY_POOL_SIZE = 100,
    SQLALCHEMY_POOL_TIMEOUT = 10,
    SQLALCHEMY_POOL_RECYCLE = 3600,
)
logger = logging.getLogger(__name__)
init_db(app)

@app.route('/')
def index():
    return 'Hello World'

@app.before_request
def before():
    user = get_current_user()
    if not user:
        return redirect(create_login_url())
