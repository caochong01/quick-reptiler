# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from bhcrjyApp.AppUtils.HttpMessageTool import HttpUtils
from bhcrjyApp.app import loginCheck
from bhcrjyApp.httpFileURIConfig import HTTP_STUDY_URI
from flask.blueprints import Blueprint
from flask import request, make_response
from flask import render_template, redirect, abort, url_for
import json

bp = Blueprint('looktax', __name__, url_prefix='/looktax')


@bp.route('/lookStudy', methods=['GET', 'POST'])
@loginCheck
def lookStudy():
    """
    查看课程学习目录
    :return:
    """
    bhcjcookies = request.cookies
    bhcjcookie = bhcjcookies.get('bhcj')
    request_resp = HttpUtils.request(tag='student_course_study3', uri=HTTP_STUDY_URI,
                                     cookies=json.loads(bhcjcookie), timeout=10)
    return request_resp
    pass


@bp.route('/tax', methods=['GET', 'POST'])
@loginCheck
def skipClass():
    """
    201909学期课题直刷3科15次
    :return:
    """
    bhcjcookies = request.cookies
    bhcjcookie = bhcjcookies.get('bhcj')
    xh = bhcjcookies.get('xh', '')
    print('刷题学号：', xh)
    request_resp = HttpUtils.request(tag='student_course_study3', uri=HTTP_STUDY_URI,
                                     cookies=json.loads(bhcjcookie), timeout=10)

    def getClass():
        soup = BeautifulSoup(request_resp.text, 'lxml')
        select = soup.select('table tr table')
        for table in select:
            td_select = table.select("td tr[align='center'] td[class='12content']")
            if len(td_select) == 9:
                reslut = []
                for i in range(len(td_select)):
                    if i < 2:
                        reslut.append(td_select[i].text.strip())
                    else:
                        reslut.append(td_select[i].a['href'])
                yield reslut

    for i in getClass():
        mapping = {
            'class3_url': i[3]
        }
        for _ in range(15):
            request_resp = HttpUtils.request(tag='enter_class3',
                                             uri=HTTP_STUDY_URI,
                                             mapping=mapping,
                                             cookies=json.loads(bhcjcookie),
                                             timeout=10)

    result = {
        'code': 200,
        'data': 'OK,skipClass success!',
    }
    return result
