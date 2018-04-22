#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/22 21:11
# @Author  : TOM.LEE
# @Site    : https://github.com/amlyj/proxyDL
# @File    : download.py
# @Software: PyCharm

import os
import platform

import requests

import settings


class ProxyDLException(Exception):
    pass


def create_or_pass_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def check_file_path(file_path):
    if os.path.exists(file_path):
        return file_path

    if platform.system() == 'Windows':
        create_or_pass_dir(settings.default_path_win)
        return settings.default_path_win

    create_or_pass_dir(settings.default_path_linux)
    return settings.default_path_linux


def build_headers():
    return {
        'Cookie': '',
        'accept-language:': 'zh-CN,zh;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'cache-control': 'max-age=0',
        'Connection': 'keep-alive',
        'upgrade-insecure-requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; '
                      'SM-G900P Build/LRX21T) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 '
                      'Mobile Safari/537.36',
    }


def download(url, cookie=""):
    headers = build_headers()
    headers['Cookie'] = cookie
    file_name = url.split("/")[-1:][0].split("?")[0]
    response = requests.get(url=url, headers=headers)
    if response.status_code not in xrange(200, 300):
        raise ProxyDLException(response.content)

    file_path = u'%s/%s' % (check_file_path(settings.download_path), file_name)
    if os.path.exists(file_path):
        return file_path

    with open(file_path, "wb") as code:
        try:
            code.write(response.content)
        except Exception, e:
            print u'下载：%s  失败! %s' % (file_path, e)
            raise ProxyDLException(e)
