#!/usr/local/bin/python2.7
#coding:utf-8

import datetime

def outdate(date):
    return datetime.date.today() > date

def votetype(t):
    if t == 0:
        return 'single'
    elif t == 1:
        return 'multiple'

