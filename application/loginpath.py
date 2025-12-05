from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os
from models.loginmodel import registerquery, loginquery
loginpath = Blueprint('loginpath', __name__, template_folder="templates")
@loginpath.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template("login.html")

@loginpath.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        user_id = request.form.get('user_id', '')
        username = request.form.get('username', '')
        user_password = request.form.get('user_password', '')

        actual_pass = generate_password_hash(user_password, method='pbkdf2:sha256')
        success, msg = registerquery(user_id, username, actual_pass)

        if success:
           
            return redirect(url_for('loginpath.login'))
        else:
        
            return render_template("register.html", msg=msg)

    return render_template("register.html", msg=msg)


@loginpath.route("/Home")
def Homepage():
    if not session.get('loggedin'):
        return render_template("loginpath.login.html")
    else:
     return render_template("Home.html")
 
@loginpath.route("/")
@loginpath.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'user_id' in request.form and 'username' in request.form and 'password' in request.form:
        
        user_id = request.form.get('user_id', '')
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        account, hps = loginquery(user_id, username) 
        
        if account and check_password_hash(hps, password):
         print("step works")
         print(account[0])
         session['loggedin'] = True
         session['id'] = account[0]
         session['username'] = account[1]
         return redirect(url_for('loginpath.Homepage'))
         
           
        else: 
            msg = "Incorrect Fields!"
            return render_template('login.html', msg=msg)
              
            
    else: 
     return render_template('login.html', msg=msg)
            
            
        
        
