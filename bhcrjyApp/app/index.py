# -*- coding: utf-8 -*-

from bhcrjyApp.AppUtils.HttpMessageTool import HttpUtils
from bhcrjyApp.app import loginCheck
from flask.blueprints import Blueprint
from flask import request, make_response
from flask import render_template, redirect, abort, url_for

bp = Blueprint('index', __name__, url_prefix='/')


@bp.route('/main_index', methods=['GET', 'POST'])
@loginCheck
def main_index():
    """
    首页展示
    :return:
    """

    response = make_response(render_template('index/index.html', skipClass=url_for('looktax.skipClass')))
    return response
