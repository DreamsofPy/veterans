
import jinja2
from flask import render_template, flash, url_for, redirect
from flask.ext import wtf
from flask.ext.wtf import validators

import re
import logging

from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView

#posts = Blueprint('posts', __name__, template_folder='templates')

from heroes import app
@app.route('/')
def hello_world(name=None):
    return render_template("home.html", name=name)

@app.route('/map')
def map(name=None):
    return render_template("home.html", name=name)

@app.route('/view')
def viewgift(name=None):
    return render_template("home.html", name=name)

@app.route('/add')
def addpost(name=None):
    return render_template("home.html", name=name)

@app.route('/tour')
def tour(name=None):
    return render_template("home.html", name=name)

@app.route('/theme')
def show_theme(name=None):
    return render_template("theme.html", name=name)

@app.errorhandler(404)
def page_not_found(e):
    """ Renders 404 Error page """
    return render_template('404.html'), 404
