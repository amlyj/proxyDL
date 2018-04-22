#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Tom.Lee
# @File           : flask_app.py
# @Product        : PyCharm
# @Docs           : main
# @Source         : 

import threading

from flask import Flask, render_template, flash, request,redirect

from app.download import download
from settings import static_folder, template_folder, debug

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

# 使用消息提示需要指定secret_key
app.secret_key = '1!@#$%^&*()'


@app.route('/', methods=["GET", "POST"])
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


@app.route('/download', methods=["POST"])
def download_handler():
    form = request.form
    url = form.get('url')
    cookie = form.get('cookie')
    if not url:
        flash(u"url 不能为空！")
        return redirect("/")

    thread = threading.Thread(target=download, kwargs={"url": url, "cookie": cookie})
    thread.start()
    flash("%s downloading ..." % url)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=debug)
