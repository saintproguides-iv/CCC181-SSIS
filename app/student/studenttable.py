from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
from dotenv import load_dotenv
import os
from app.models.smodel import get_students, base_students, creates, updates, deletes
from werkzeug.utils import secure_filename
from supabase import create_client

student_bp = Blueprint('student_bp', __name__, template_folder="../templates")
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
)
    
    return conn
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "uploads")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@student_bp.route('/Student')
def Home():
     if not session.get('loggedin'):
        return render_template("login.html")
     else:
        prog , msg2 = base_students()
        return render_template("Student.html", prog=prog, msg2=msg2)
       

@student_bp.route('/students_data')
def students_data():
    draw = request.args.get('draw', type=int, default=1)
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)
    search_value = request.args.get('search[value]', type=str)

    order_column_index = request.args.get('order[0][column]', type=int)
    order_dir = request.args.get('order[0][dir]', type=str, default='asc')

    columns = [
        "Students.student_image",
        "s_id",
        "First_Name",
        "Last_Name",
        "Students.gender",
        "Students.Program_ID",
        "Programs.Program_Name",
        "Students.year_level"
    ]
    order_column = columns[order_column_index] if order_column_index is not None else "s_id"

    data, records_total, records_filtered = get_students(start, length, search_value, order_column, order_dir)

    return jsonify({
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'data': data
    })
@student_bp.route('/s_create', methods=['POST'])
def create():
    
   
    s_id = request.form['s_id']
    First_Name = request.form['First_Name']
    Last_Name = request.form['Last_Name']
    Program_ID = request.form['Program_ID']
    Gender = request.form['Gender']
    Year_Level = request.form['Year Level']
    profpic_file = request.files.get("profilePictureUpload")
    msg2 = creates(s_id, First_Name, Last_Name,Program_ID,Gender,Year_Level,profpic_file)
    return redirect(url_for('student_bp.Home', msg2=msg2)) 


@student_bp.route('/s_update', methods=['POST'])
def update():
    s_id = request.form['s_id']
    First_Name = request.form['First_Name']
    Last_Name = request.form['Last_Name']
    Program_ID = request.form['Program_ID']
    Gender = request.form['Gender']
    Year_Level = request.form['Year Level']
    profpic_file = request.files.get("profilePictureUpload")
    msg2 = updates(s_id, First_Name, Last_Name,Program_ID,Gender,Year_Level,profpic_file)
    return redirect(url_for('student_bp.Home',msg2=msg2))


@student_bp.route('/s_delete', methods=['POST'])
def delete():
    s_id = request.form['s_id']
    deletes(s_id)
    return redirect(url_for('student_bp.Home',))