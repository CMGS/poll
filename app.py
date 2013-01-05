import config
import logging
from flask import Flask, redirect, url_for, \
        g, request, render_template

from dae.api.users import get_current_user, create_login_url

from models import init_db
from query import get_subjects, get_votes, \
        update_votes
from utils import outdate, votetype

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.config.update(
    SQLALCHEMY_DATABASE_URI = config.DATABASE_URI,
    SQLALCHEMY_POOL_SIZE = 100,
    SQLALCHEMY_POOL_TIMEOUT = 10,
    SQLALCHEMY_POOL_RECYCLE = 3600,
)
app.jinja_env.globals['outdate'] = outdate
app.jinja_env.globals['votetype'] = votetype

logger = logging.getLogger(__name__)
init_db(app)

@app.route('/')
def index():
    q = request.args.get('q', '')
    return render_template('index.html', subjects=get_subjects(q))

@app.route('/view/<int:sid>/')
def view(sid):
    votes = get_votes(sid)
    if not votes:
        return redirect(url_for('index'))
    subject = votes[0].subject
    return render_template('view.html', subject=subject, \
            votes=votes)

@app.route('/vote/<int:sid>/', methods=['POST'])
def vote(sid):
    votes = request.form
    if votes:
        update_votes(votes.listvalues()[0])
    return redirect(url_for('view', sid=sid))

@app.before_request
def before():
    user = get_current_user()
    if not user:
        return redirect(create_login_url())
    g.user = user

