from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
import os
import config
from supabase import create_client
from werkzeug.utils import secure_filename

def programs_base():
    conn = config.get_db_connection()
    cur = conn.cursor()
    msg2 = request.args.get('msg2', '')
              
    cur.execute(
 '''SELECT DISTINCT College_ID FROM colleges''')
    
    clg = cur.fetchall()
    cur.close()
    conn.close()
    return clg, msg2
def get_programs(start, length, search_value, order_column, order_dir):
    conn = config.get_db_connection()
    
    cur = conn.cursor()

    base_query = '''
        SELECT program_id, program_name, COALESCE(college_in, 'No College') FROM programs
    '''
    params = []

    if search_value:
        base_query += "WHERE program_id ILIKE %s OR program_name ILIKE %s OR college_in ILIKE %s"
        params.extend([f"%{search_value}%", f"%{search_value}%", f"%{search_value}%"])

    base_query += f" ORDER BY {order_column} {order_dir.upper()} LIMIT %s OFFSET %s"
    params.extend([length, start])

    cur.execute(base_query, tuple(params))
    data = cur.fetchall()

  
    cur.execute("SELECT COUNT(*) FROM Programs")
    records_total = cur.fetchone()[0]

    if search_value:
        cur.execute("SELECT COUNT(*) FROM programs WHERE program_id ILIKE %s OR program_name ILIKE %s OR college_in ILIKE %s",
                    (f"%{search_value}%", f"%{search_value}%", f"%{search_value}%"))
        records_filtered = cur.fetchone()[0]
    else:
        records_filtered = records_total

    cur.close()
    conn.close()

    return data, records_total, records_filtered

def pcreate(program_id, program_name, college_in):
    conn = config.get_db_connection()

    cur = conn.cursor()
    msg2 = ''
    if not program_id or not program_name or not college_in:
          msg2 = "Required fields missing"
          return msg2
    else:
            cur.execute(
            '''INSERT INTO programs (program_id, program_name, college_in) VALUES (%s, %s, %s)''',
            (program_id, program_name, college_in))
    conn.commit()
    msg2 = f'Program {program_id} succesfully inserted'
        
    return msg2
def pupdate(program_id, program_name, college_in):
    conn = config.get_db_connection()
    
    cur = conn.cursor()
    cur.execute(
        '''UPDATE programs SET program_name=%s, \
         college_in=%s WHERE program_id=%s ''', (program_name, college_in, program_id ))
 
    msg2 = f'Program {program_id} succesfully updated'
    conn.commit()
    cur.close()
    conn.close()
    return msg2
    
def pdelete(program_id):
    conn = config.get_db_connection()
    cur = conn.cursor()
    cur.execute('''DELETE FROM programs WHERE program_id=%s''', (program_id,))

    msg2 = f'Program {program_id} succesfully deleted'
    conn.commit()

   
    cur.close()
    conn.close()
    return msg2
    