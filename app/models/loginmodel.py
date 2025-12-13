from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
import os
from supabase import create_client
from werkzeug.utils import secure_filename
import config


def registerquery(user_id, username, actual_pass):
 try:
    conn = config.get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        conn.close()
        return False, "User ID is invalid. Please choose a different one."
    else:
        cur.execute(
            '''INSERT INTO users (user_id, username, user_password)
               VALUES (%s, %s, %s)''',
            (user_id, username, actual_pass))
        conn.commit()
        cur.close()
        conn.close()
        return True, None
 except psycopg2.Error:
     return False, "User ID is invalid. Please choose a different one."



def loginquery(user_id, username,):
    conn = config.get_db_connection()
    cur = conn.cursor()
    account = None
    hps = None
    
    
    
        
        
    cur.execute('SELECT * FROM users WHERE user_id = %s AND username = %s', (user_id, username))
    account = cur.fetchone() 
    cur.execute('SELECT user_password FROM users WHERE user_id = %s AND username = %s', (user_id, username))
    hashpass = cur.fetchone() 
    hps = hashpass[0] if hashpass else None
    cur.close()
    conn.close()
    return account,hps
        
        
   