# -*- coding: utf-8 -*-
import functools

from bhcrjyApp.redisConfig import redis_db
from flask import request, make_response
from flask import url_for, render_template, redirect


def loginCheck(func):
    """
    登录检查
    :return:
    """

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        bhcjcookies = request.cookies
        userId = bhcjcookies.get('userId')
        if userId:
            bhcjcookie = redis_db.connection.get(userId)
            if bhcjcookie is not None:
                redis_db.connection.expire(userId, 1800)
                return func(*args, **kwargs)

        return redirect(url_for('login.indexLogin'))

    # 装饰器
    return decorator
