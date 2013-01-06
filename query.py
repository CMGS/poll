#!/usr/local/bin/python2.7
#coding:utf-8

from models import Subject, Vote, Group
from sqlalchemy.sql.expression import asc

def get_subjects(q):
    if not q:
        return Subject.query.order_by(asc(Subject.deadline)).all()
    return Subject.query.filter_by(group=q).order_by(asc(Subject.deadline)).all()

def get_votes(sid):
    return Vote.query.filter_by(sid=sid).all()

def get_groups():
    return Group.query.all()

def get_group(gid):
    if not gid:
        return None
    return Group.query.get(gid)

def update_votes(votes):
    for vid in votes:
        vote = Vote.query.get(vid)
        vote.incr()

def create_subject(topic, group, deadline, votetype, options):
    if not get_group(group):
        raise Exception('Group not exist')
    if votetype not in ['0', '1']:
        raise Exception('Vote type error')
    options = [o for o in options if o]
    if not options:
        raise Exception('No options')
    subject = Subject.create(topic, deadline, votetype, group)
    for option in options:
        Vote.create(subject.id, option)

