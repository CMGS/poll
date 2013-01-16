#!/usr/local/bin/python2.7
#coding:utf-8

import datetime
from utils import outdate
from models import Subject, Vote, Group
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

def update_votes(sid, votes):
    subject = Subject.query.get(sid)
    if not subject or outdate(subject.deadline):
        raise Exception('Invaild Subject')
    for vid in votes:
        vote = Vote.query.get(vid)
        vote.incr()

def create_subject(topic, group, deadline, votetype, options, creator):
    if not topic:
        raise Exception('Topic is necessary')
    if not get_group(group):
        raise Exception('Group not exist')
    if votetype not in ['0', '1']:
        raise Exception('Vote type error')
    options = [o for o in options if o]
    if len(options) < 2:
        raise Exception('No options')
    subject = Subject.create(topic, deadline, votetype, group, creator)
    for option in options:
        Vote.create(subject.id, option)

