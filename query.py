#!/usr/local/bin/python2.7
#coding:utf-8

from models import Subject, Vote

def get_subjects(q):
    if not q:
        return Subject.query.all()
    return Subject.query.filter_by(group=q).all()

def get_votes(sid):
    return Vote.query.filter_by(sid=sid).all()

def update_votes(votes):
    for vid in votes:
        vote = Vote.query.get(vid)
        vote.incr()

