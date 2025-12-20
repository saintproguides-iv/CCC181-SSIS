from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2
from app.models.pmodel import programs_base,get_programs, pcreate, pupdate, pdelete
import os
program_bp = Blueprint('program_bp', __name__, template_folder="../templates")
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
)
    
    return conn
@program_bp.route('/Programs')
def Home():              
 if not session.get('loggedin'):
        
       return render_template("login.html")
 else: 
       clg, msg2 = programs_base()
       return render_template("Programs.html", clg = clg, msg2=msg2)
   
 
  
 
  
        
             
     
@program_bp.route('/programs_data')
def programs_data():
    program = request.args.get('program', 'All Programs')
    draw = request.args.get('draw', type=int, default=1)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)

    order_column_index = request.args.get('order[0][column]', type=int)
    order_dir = request.args.get('order[0][dir]', type=str, default='desc')

    columns = [
        "program_id",
        "program_name",
        "college_in"
    ]
    order_column = columns[order_column_index] if order_column_index is not None else "program_id"

    data, records_total, records_filtered = get_programs(start, length, search_value, order_column, order_dir)

    return jsonify({
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'data': data
    })
    
@program_bp.route('/p_create', methods=['POST'])
def create():
    print("CREATE ROUTE HIT!") 
    conn = None
    cur = None
    try:
        
       
        program_id = request.form['program_id']
        program_name = request.form['program_name']
        college_in = request.form['college_in']
        msg2 = pcreate(program_id, program_name, college_in)
        
     
    except psycopg2.Error as e:
        print(f"Program ID already exists")  
        if conn:  
            conn.rollback()
        msg2 = f"Program ID already exists" 
        return redirect(url_for('program_bp.Home', msg2=msg2)) 
    
    except Exception as e:
        print(f"GENERAL ERROR: Something went wrong.")  
        if conn:
            conn.rollback()
        msg2 = f"GENERAL ERROR: Something went wrong."
        return redirect(url_for('program_bp.Home', msg2=msg2))
    
    finally:
        if cur:  
            cur.close()
        if conn: 
            conn.close()
    return redirect(url_for('program_bp.Home', msg2=msg2))

    


@program_bp.route('/p_update', methods=['POST'])
def update():
    
    program_id = request.form['program_id']
    program_name = request.form['program_name']
    college_in = request.form['college_in']
    msg2 = pupdate(program_id, program_name, college_in)
    return redirect(url_for('program_bp.Home', msg2=msg2))


@program_bp.route('/p_delete', methods=['POST'])
def delete():
    program_id = request.form['program_id']
    msg2 = pdelete(program_id)
    return redirect(url_for('program_bp.Home', msg2=msg2))