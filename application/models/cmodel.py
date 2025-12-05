from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
import os
from supabase import create_client
from werkzeug.utils import secure_filename
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
)
    return conn
def get_colleges():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
               msg2 = request.args.get('msg2', '')
              
             
  
        
               cur.execute('''SELECT * FROM colleges''', 
                   )
               items_on_page = cur.fetchall()
               return  items_on_page,msg2
    except psycopg2.Error as e:
               conn.rollback()
               return f"Database error: {str(e)}", 400
    finally:
            cur.close()
            conn.close()
def ccreate(college_id, college_name):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        msg2 = ''
        
        
        if not college_id or not college_name:
          msg2 = "Required fields missing"
        else:
          
          cur.execute(
            '''INSERT INTO colleges (college_id, college_name) VALUES (%s, %s)''',
            (college_id, college_name))
          conn.commit()
        print("Insert successful!")
        
        return msg2
     
    except psycopg2.Error as e:
        print(f"DATABASE ERROR: {e}")  
        if conn:  
            conn.rollback()
        msg2 = f'Error! {e}'  
        return msg2
    
    except Exception as e:
        print(f"GENERAL ERROR: {e}")  # CATCH OTHER ERRORS
        if conn:
            conn.rollback()
        msg2 = f'Error! {e}'
        return  msg2
    
    finally:
        if cur:  # CHECK IF cur EXISTS BEFORE CLOSING
            cur.close()
        if conn:  # CHECK IF conn EXISTS BEFORE CLOSING
            conn.close()
def cupdate(college_name, college_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''UPDATE colleges SET college_name=%s WHERE college_id=%s ''', (college_name, college_id ))
    conn.commit()
    cur.close()
    conn.close()
   

def cdelete(college_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''DELETE FROM colleges WHERE college_id=%s''', (college_id, ))

   
    conn.commit()

   
    cur.close()
    conn.close()
    