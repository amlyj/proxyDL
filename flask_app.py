#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author         : Tom.Lee
# @File           : flask_app.py
# @Product        : PyCharm
# @Docs           : main
# @Source         : 

from app import app, debug

if __name__ == "__main__":
    app.run(debug=debug)
