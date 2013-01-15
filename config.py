#!/usr/local/bin/python2.7
#coding:utf-8

DEBUG = True
DATABASE_URI = 'mysql://'
SECRET_KEY = '!@$vote!#$%^'
SESSION_KEY = 'xid'
SESSION_COOKIE_DOMAIN = '127.0.0.1'

try:
    from local_config import *
except:
    pass
