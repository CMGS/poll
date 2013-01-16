#!/usr/local/bin/python2.7
#coding:utf-8

import datetime

def isban(sid, name):
    from query import get_ban
    return bool(get_ban(sid, name))

def outdate(date):
    return datetime.date.today() > date

def votetype(t):
    if t == 0:
        return 'single'
    elif t == 1:
        return 'multiple'

