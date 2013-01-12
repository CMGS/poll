import config
import logging
from flask import Flask, redirect, url_for, \
        g, request, render_template

from sheep.api.users import get_current_user, \
        generate_login_url
from sheep.api.sessions import SessionMiddleware, \
    FilesystemSessionStore

from models import init_db
from query import get_subjects, get_votes, \
        update_votes, get_groups, get_group, \
        create_subject
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
app.wsgi_app = SessionMiddleware(app.wsgi_app, \
        FilesystemSessionStore(), \
        cookie_name=config.SESSION_KEY, cookie_path='/', \
        cookie_domain=config.SESSION_COOKIE_DOMAIN)

@app.route('/')
def index():
    q = request.args.get('q', '')
    inprogress, closed = get_subjects(q)
    return render_template('index.html', user=g.user, \
            inprogress = inprogress, \
            closed = closed, \
            groups=get_groups(), \
            group=get_group(q))

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
        update_votes(votes.getlist('selected'))
    return redirect(url_for('view', sid=sid))

@app.route('/write/', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html', user=g.user, \
                groups=get_groups())
    topic = request.form.get('topic')
    group = request.form.get('group')
    deadline = request.form.get('deadline')
    votetype = request.form.get('votetype')
    options = request.form.getlist('options')
    create_subject(topic, group, deadline, votetype, options)
    return redirect(url_for('index', q=group))

@app.before_request
def before():
    user = get_current_user(request.environ['xiaomen.session'])
    if not user:
        return redirect(generate_login_url())
    g.user = user

