#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.run import app
from flask import render_template


@app.route("/ss")
def ss():
    return render_template('index.html')
