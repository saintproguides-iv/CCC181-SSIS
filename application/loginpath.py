from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
from flask_login import LoginManager

import psycopg2
import os
from models.loginmodel import registerquery, loginquery
loginpath = Blueprint('loginpath', __name__, template_folder="templates")
@loginpath.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('loginpath.login'))

@loginpath.route('/register', methods=['GET', 'POST'])
def register():
    return registerquery()
@loginpath.route("/Home")
def Homepage():
    if not session.get('loggedin'):
        return render_template("loginpath.login.html")
    else:
     return render_template("Home.html")
@loginpath.route("/")
@loginpath.route('/login', methods=['GET', 'POST'])
def login():
        return loginquery()