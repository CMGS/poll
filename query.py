#!/usr/local/bin/python2.7
#coding:utf-8

from models import Subject, Vote, Group

def get_subjects(q):
    if not q:
        return Subject.query.all()
    return Subject.query.filter_by(group=q).all()

def get_votes(sid):
    return Vote.query.filter_by(sid=sid).all()

def get_groups():
    return Group.query.all()

def update_votes(votes):
    for vid in votes:
        vote = Vote.query.get(vid)
        vote.incr()

def create_subject(topic, group, deadline, votetype, options):
    if not Group.query.get(group):
        raise Exception('Group not exist')
    if votetype not in ['0', '1']:
        raise Exception('Vote type error')
    options = [o for o in options if o]
    if not options:
        raise Exception('No options')
    subject = Subject.create(topic, deadline, votetype, group)
    for option in options:
        Vote.create(subject.id, option)

