import config
import logging
from flask import Flask, redirect, url_for, \
        g, request, render_template

from dae.api.users import get_current_user, \
        create_login_url

from models import init_db
from query import get_subjects, get_votes, \
        update_votes, get_groups, get_group, \
        create_subject
from utils import outdate, votetype, isban

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.config.update(
    SQLALCHEMY_DATABASE_URI = config.DATABASE_URI,
    SQLALCHEMY_POOL_SIZE = 100,
    SQLALCHEMY_POOL_TIMEOUT = 10,
    SQLALCHEMY_POOL_RECYCLE = 3600,
)
app.jinja_env.globals['isban'] = isban
app.jinja_env.globals['outdate'] = outdate
app.jinja_env.globals['votetype'] = votetype

logger = logging.getLogger(__name__)
init_db(app)

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
    msg = request.args.get('msg', '')
    if not votes:
        return redirect(url_for('index'))
    subject = votes[0].subject
    q = '' or subject.groupobj.id
    sum_count = sum([v.count for v in votes])
    return render_template('view.html', subject=subject, \
            votes=votes, sum = sum_count, q = q, \
            msg = msg)

@app.route('/vote/<int:sid>/', methods=['POST'])
def vote(sid):
    votes = request.form
    msg = ''
    try:
        update_votes(sid, votes.getlist('selected'), g.user.username)
    except Exception, e:
        msg = str(e)
    return redirect(url_for('view', sid=sid, msg=msg))

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
    try:
        create_subject(topic, group, deadline, votetype, options, g.user.username)
    except Exception, e:
        return render_template('write.html', user=g.user, \
                groups=get_groups(), exc=str(e))
    else:
        return redirect(url_for('index', q=group))

@app.before_request
def before():
    user = get_current_user()
    if not user:
        return redirect(create_login_url())
    g.user = user

