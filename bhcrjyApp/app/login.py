# -*- coding: utf-8 -*-
import uuid
from bhcrjyApp.AppUtils.HttpMessageTool import HttpUtils
from bhcrjyApp.app import loginCheck
from bhcrjyApp.app.user import get_user_info
from bhcrjyApp.httpFileURIConfig import HTTP_LOGIN_URI
from bhcrjyApp.redisConfig import redis_db
from flask.blueprints import Blueprint
from flask import request, make_response
from flask import render_template, abort, url_for, redirect
import requests
import json
import os

bp = Blueprint("login", __name__, url_prefix="/login")


@bp.route('/', methods=['GET', 'POST'])
def indexLogin():
    """
    登录页面返回，及北航校网cookie获取
    :return: login页面
    """
    bhcjcookies = request.cookies
    userId = bhcjcookies.get('userId')
    if userId:
        bhcjcookie = redis_db.connection.get(userId)
        if bhcjcookie is not None:
            redis_db.connection.expire(userId, 1800)
            return redirect(url_for('index.main_index'))
    print(os.getcwd())
    request_resp = HttpUtils.request(tag='login_new', uri=HTTP_LOGIN_URI,
                                     allow_redirects=False, timeout=10)

    uuid_user = uuid.uuid1()
    jsonCookie = json.dumps(requests.utils.dict_from_cookiejar(request_resp.cookies))
    response = make_response(render_template('login/login.html', imgdata='image'))
    response.set_cookie('userId', str(uuid_user))
    response.set_cookie('bhcj', jsonCookie)
    return response


@bp.route('/image', methods=['GET', 'POST'])
def indeximage():
    """
    北航校网登录验证码获取，遵循校网标准
    :return: 二进制验证码图片
    """
    bhcjcookies = request.cookies
    bhcjcookie = bhcjcookies.get('bhcj')

    request_resp = HttpUtils.request(tag='login_new_image', uri=HTTP_LOGIN_URI,
                                     cookies=json.loads(bhcjcookie), timeout=10)

    response = make_response(request_resp.content)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@bp.route('/login', methods=['POST'])
def login():
    """
    将登录信息发送至北航校网进行验证
    :return: 登录状态
    """
    bhcjcookies = request.cookies
    bhcjcookie = bhcjcookies.get('bhcj')

    body = {
        'login_id': request.form['studentId'],
        'input_password': request.form['password'],
        'type': 'STUDENT',
        'rand': request.form['yzm'],
    }
    request_resp0 = HttpUtils.request(tag='login', uri=HTTP_LOGIN_URI, body=body,
                                      cookies=json.loads(bhcjcookie),
                                      allow_redirects=False, timeout=10)
    request_resp = HttpUtils.request(tag='enter', uri=HTTP_LOGIN_URI,
                                     cookies=json.loads(bhcjcookie),
                                     allow_redirects=False, timeout=10)
    if request_resp.status_code == 302:
        redis_db.connection.set(bhcjcookies.get('userId'), bhcjcookie, ex=1800)
        response = make_response({'code': 200, 'localhost': url_for('index.main_index')})

        # 用户基本信息获取，方便后续推送功能上线
        xh = request.form['studentId']
        response.set_cookie('xh', xh)
        try:
            user_info = [i for i in get_user_info()]
            print(F'登录[{xh}]:', user_info)
            result = json.dumps(user_info).encode('utf-8')
            redis_db.connection.set(xh, result)
        except Exception as e:
            print(F'<ERROR> 获取用户信息异常[{xh}]:', e)

        return response
    elif request_resp.status_code == 200:
        return make_response({'code': 302, 'localhost': url_for('login.indexLogin')})

    return abort(401)


@bp.route('/logout', methods=['GET', 'POST'])
@loginCheck
def logout():
    """
    将注销信息发送至北航校网进行退出
    :return: 重定向至登录页面
    """
    bhcjcookies = request.cookies
    redis_db.connection.delete(bhcjcookies.get('userId'))
    return redirect(url_for('login.indexLogin'))
