# -*- coding: utf-8 -*-
from flask import session,redirect,url_for
from functools import wraps
#登录访问
def longin_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper