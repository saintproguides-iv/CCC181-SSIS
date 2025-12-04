from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
import os
from werkzeug.security import generate_password_hash
from supabase import create_client
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
)
    return conn


def registerquery():
    
 msg = '' 
 try:
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        
        
        user_id = request.form['user_id']
        username = request.form['Username']
        user_password = request.form['user_password'] 
        actual_pass = generate_password_hash(user_password, method='pbkdf2:sha256')   
        cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()     
        if existing_user:
                cur.close()
                conn.close() 
                msg = 'User ID is invalid. Please choose a different one.'  
  
                    
        else:
                cur.execute(
                    '''INSERT INTO users \
                    (user_id, username, user_password) VALUES (%s,%s, %s)''',
                    (user_id, username, actual_pass))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('loginpath.login'))
 except:
     msg = 'User ID is invalid. Please choose a different one.'  
 return render_template("register.html", msg=msg)
   

def loginquery():
    conn = get_db_connection()
    cur = conn.cursor()

    msg = ''
    if request.method == 'POST' and 'user_id' in request.form and 'username' in request.form and 'password' in request.form:
        user_id = request.form['user_id']
        username = request.form['username']
        password = request.form['password']
        
        cur.execute('SELECT * FROM users WHERE user_id = %s AND username = %s', (user_id, username))
        account = cur.fetchone()
        cur.execute('SELECT user_password FROM users WHERE user_id = %s AND username = %s', (user_id, username))
        hashpass = cur.fetchone()
        if account and check_password_hash(hashpass[0], password):
         print("step works")
         print(account[0])
         session['loggedin'] = True
         session['id'] = account[0]
         session['username'] = account[1]
         return redirect(url_for('loginpath.Homepage'))
         
           
        else:
            msg = 'Incorrect fields!'
    return render_template('login.html', msg=msg)