#!/usr/local/bin/python2.7
#coding:utf-8

import datetime
from utils import outdate, \
        check_subject_params
from models import Subject, Vote, Group, Ban
from sqlalchemy.sql.expression import asc

def get_subjects(q):
    today = datetime.date.today()
    if not q:
        inprogress = Subject.query.filter(Subject.deadline >= today).order_by(asc(Subject.deadline)).all()
        closed = Subject.query.filter(Subject.deadline < today).order_by(asc(Subject.deadline)).all() 
        return inprogress, closed
    inprogress = Subject.query.filter_by(group=q).filter(Subject.deadline >= today).order_by(asc(Subject.deadline)).all()
    closed = Subject.query.filter_by(group=q).filter(Subject.deadline < today).order_by(asc(Subject.deadline)).all()
    return inprogress, closed

def get_votes(sid):
    return Vote.query.filter_by(sid=sid).all()

def get_groups():
    return Group.query.all()

def get_group(gid):
    if not gid:
        return None
    return Group.query.get(gid)

def get_subject(sid):
    if not sid:
        return None
    return Subject.query.get(sid)

def get_ban(sid, name):
    return Ban.query.filter(Ban.sid==sid, Ban.name==name).limit(1).first()

def update_votes(sid, votes, name):
    if not votes:
        raise Exception('Invaild votes')
    subject = Subject.query.get(sid)
    if not subject or outdate(subject.deadline):
        raise Exception('Invaild subject')
    if get_ban(sid, name):
        raise Exception('Vote only once')
    for vid in votes:
        vote = Vote.query.get(vid)
        vote.incr()
    Ban.create(sid, name)

def create_subject(topic, group, deadline, votetype, options, creator):
    options = check_subject_params(topic, get_group(group), deadline, votetype, options)
    subject = Subject.create(topic, deadline, votetype, group, creator)
    for option in options:
        Vote.create(subject.id, option)

def modify_subject(subject, topic, group, deadline, votetype, options, optionsid):
    # DO NOT ESCAPE OPTIONS CAUSE IT CONTAINS OLD AND NEW OPTION
    check_subject_params(topic, get_group(group), deadline, votetype, options)
    subject.modify(topic, deadline, votetype, group)
    for i in range(len(optionsid)):
        vote = Vote.query.get(optionsid[i])
        if not options[i]:
            vote.delete()
        elif options[i] != vote.content:
            vote.update(options[i])
    options = [o for o in options[i+1:] if o]
    for option in options:
        Vote.create(subject.id, option)

