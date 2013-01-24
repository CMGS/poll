#!/usr/local/bin/python2.7
#coding:utf-8

import datetime

PATTERN = r'(\d+)/*$'

def outdate(date):
    if not date:
        return True
    return datetime.date.today() > date

def votetype(t):
    if t == 0:
        return 'single'
    elif t == 1:
        return 'multiple'

def check_subject_params(topic, group, deadline, votetype, options):
    if not topic:
        raise Exception('Topic is necessary')
    if not group:
        raise Exception('Group not exist')
    if votetype not in ['0', '1']:
        raise Exception('Vote type error')
    if not deadline:
        raise Exception('Not valid deadline')
    else:
        datetime.datetime.strptime(deadline, '%Y-%m-%d')
    options = [o for o in options if o]
    if len(options) < 2:
        raise Exception('Invaild options number')
    return options
