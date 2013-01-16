#!/usr/local/bin/python2.7
#coding:utf-8

DEBUG = True
DATABASE_URI = 'mysql://'
SECRET_KEY = '!@$vote!#$%^'

try:
    from local_config import *
except:
    pass
