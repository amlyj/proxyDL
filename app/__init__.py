#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/22 14:29
# @Author  : TOM.LEE
# @Site    : https://github.com/amlyj/proxyDL
# @File    : __init__.py.py
# @Software: PyCharm
import threading

from flask import Flask, render_template, flash, request, redirect, abort

from app.download import download, download_proxy, local_file, ProxyDLException
from settings import static_folder, template_folder, debug

_ = debug
# 设置访问根路径
root_url = '/proxyDL'

app = Flask(__name__,
            static_path=root_url + '/static',
            static_url_path=root_url,
            static_folder=static_folder,
            template_folder=template_folder,
            instance_path=root_url)

# 使用消息提示需要指定secret_key
app.secret_key = '1!@#$%^&*()'


@app.route('/', methods=["GET"])
def home():
    return redirect(root_url)


@app.route(root_url, methods=["GET", "POST"])
def index():
    """
    使用flash来进行消息提示推送
    页面使用{{ get_flashed_messages()[0] }} 获取
    """
    flash("welcome !")
    return render_template("index.html")


@app.errorhandler(404)
def not_found(e):
    """
    404 页面
    :param e:  必须要传递一个参数, 不管是否使用该参数
    """
    return render_template("404.html", err=e)


@app.errorhandler(500)
def server_error(e):
    """
    500 页面
    :param e:
    :return:
    """
    return render_template("500.html", err=e)


@app.route(root_url + '/download', methods=["POST", "GET"])
def download_handler():
    if request.method == 'GET':
        return download_local_file(request.args.get('file_name'))
    form = request.form
    url = form.get('url')
    cookie = form.get('cookie')
    if not url:
        flash(u"url 不能为空！")
        return redirect(root_url)

    thread = threading.Thread(target=download, kwargs={"url": url, "cookie": cookie})
    thread.start()
    flash("%s downloading ..." % url)
    return redirect(root_url)


@app.route(root_url + "/download/proxy", methods=["POST"])
def download_proxy_file():
    form = request.form
    url = form.get('url')
    cookie = form.get('cookie')
    if not url:
        flash(u"url 不能为空！")
        return redirect(root_url)
    return download_proxy(url, cookie)


def download_local_file(file_name):
    try:
        return local_file(file_name)
    except ProxyDLException:
        abort(403)
