#!/usr/local/bin/python2.7
#coding:utf-8

from sqlalchemy.dialects.mysql import BIT
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def init_db(app):
    db.init_app(app)
    db.app = app
    db.create_all()

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.CHAR(16), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    votetype = db.Column(BIT(1), nullable=False, default=0)
    group = db.Column(db.Integer, index=True, nullable=False)

    def __init__(self, topic, deadline, votetype, group):
        self.topic = topic
        self.deadline = deadline
        self.votetype = votetype
        self.group = group

    @staticmethod
    def create(topic, deadline, votetype, group):
        subject = Subject(topic, deadline, votetype, group)
        db.session.add(subject)
        db.session.commit()
        return subject

class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    tid = db.Column(db.Integer, index=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    count = db.Column(db.Integer, index=True, nullable=False, default=0)

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

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.CHAR(16), nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def create(name):
        group = Group(name)
        db.session.add(group)
        db.session.commit()
        return group
