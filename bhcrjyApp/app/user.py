# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from bhcrjyApp.AppUtils.HttpMessageTool import HttpUtils
from bhcrjyApp.app import loginCheck
from bhcrjyApp.httpFileURIConfig import HTTP_USER_URI
from flask.blueprints import Blueprint
from flask import request, make_response
from flask import render_template, redirect, abort, url_for
import json

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/userinfo', methods=['GET', 'POST'])
@loginCheck
def userinfo():
    """
    用户基本信息获取
    :return:
    """
    xh = request.cookies.get('xh')
    user_info = [i for i in get_user_info()]
    result = {
        'student': xh,
        'info': user_info
    }
    return result


def get_user_info():
    """
    用户信息获取
    :return: 信息列表迭代器
    """
    bhcjcookies = request.cookies
    bhcjcookie = bhcjcookies.get('bhcj')

    request_resp = HttpUtils.request('student_info', uri=HTTP_USER_URI,
                                     cookies=json.loads(bhcjcookie),
                                     allow_redirects=False, timeout=10)
    soup = BeautifulSoup(request_resp.text.encode('utf-8'), 'lxml')
    select = soup.select("table tr table tr[valign='middle']")
    for tr_select in select:
        tds = tr_select.select('td')
        yield [td.text.replace('\n', '')
                   .replace('\xa0', '')
                   .replace('\t', '')
                   .replace('\r', '')
                   .replace('*', '')
                   .replace('：', '')
               for td in
               tds if len(tds) == 2]
