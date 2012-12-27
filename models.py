#!/usr/local/bin/python2.7
#coding:utf-8

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.CHAR(16), nullable=False)

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def create(name):
        group = Group(name)
        db.session.add(group)
        db.session.commit()
        return group

    def __unicode__(self):
        return self.name

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.CHAR(16), nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    votetype = db.Column(db.Integer, nullable=False, default=1)
    group = db.Column(db.Integer, db.ForeignKey(Group.id))
    groupname = db.relationship(Group, backref='subject')

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def create(topic, deadline, votetype, group):
        subject = Subject(topic, deadline, votetype, group)
        db.session.add(subject)
        db.session.commit()
        return subject

    def __unicode__(self):
        return self.topic

class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    count = db.Column(db.Integer, nullable=False, index=True, default=0)
    sid = db.Column(db.Integer, db.ForeignKey(Subject.id))
    subject = db.relationship(Subject, backref='vote')

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    @staticmethod
    def create(tid, content):
        vote = Vote(tid=tid, content=content)
        db.session.add(vote)
        db.session.commit()
        return vote

    def incr(self):
        self.count = Vote.count + 1
        db.session.add(self)
        db.session.commit()
        return self

