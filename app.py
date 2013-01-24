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
        create_subject, get_ban, get_subject, \
        modify_subject
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

#TODO in sheep env, do not use user.name!use user.uid!

@app.route('/')
def index():
    q = request.args.get('q', '')
    inprogress, closed = get_subjects(q)
    return render_template('index.html', \
            inprogress = inprogress, \
            closed = closed, \
            groups=get_groups(), \
            group=get_group(q), \
            q=q)

@app.route('/view/<int:sid>/')
def view(sid):
    votes = get_votes(sid)
    msg = request.args.get('msg', '')
    if not votes:
        return redirect(url_for('index'))
    subject = votes[0].subject
    q = '' or subject.groupobj.id
    sum_count = sum([v.count for v in votes])
    ban = get_ban(subject.id, g.user.name)
    modify = subject.creator == g.user.name
    return render_template('view.html', subject=subject, \
            votes=votes, sum = sum_count, q = q, \
            msg = msg, ban = ban, modify = modify)

@app.route('/vote/<int:sid>/', methods=['POST'])
def vote(sid):
    votes = request.form
    msg = ''
    try:
        update_votes(sid, votes.getlist('selected'), g.user.name)
    except Exception, e:
        msg = str(e)
    return redirect(url_for('view', sid=sid, msg=msg))

@app.route('/write/', methods=['GET', 'POST'])
def write():
    if request.method == 'GET':
        return render_template('write.html', groups=get_groups())
    topic = request.form.get('topic')
    group = request.form.get('group')
    deadline = request.form.get('deadline')
    votetype = request.form.get('votetype')
    options = request.form.getlist('options')
    try:
        create_subject(topic, group, deadline, votetype, options, g.user.name)
    except Exception, e:
        return render_template('write.html', groups=get_groups(), exc=str(e))
    else:
        return redirect(url_for('index', q=group))

@app.route('/modify/<int:sid>/', methods=['GET', 'POST'])
def modify(sid):
    subject = get_subject(sid)
    if not subject or subject.creator != g.user.name:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('modify.html', subject=subject, \
                groups=get_groups(), votes=get_votes(sid))
    topic = request.form.get('topic')
    group = request.form.get('group')
    deadline = request.form.get('deadline')
    votetype = request.form.get('votetype')
    options = request.form.getlist('options')
    optionsid = request.form.getlist('optionsid')
    try:
        modify_subject(subject, topic, group, deadline, votetype, options, optionsid)
    except Exception, e:
        return render_template('modify.html', subject=subject, \
                groups=get_groups(), votes=get_votes(sid), exc=str(e))
    else:
        return redirect(url_for('view', sid=subject.id))

@app.before_request
def before():
    user = get_current_user(request.environ['xiaomen.session'])
    if not user:
        return redirect(generate_login_url())
    g.user = user

