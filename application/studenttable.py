from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from supabase import create_client

student_bp = Blueprint('student_bp', __name__, template_folder="templates")
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
          try:
               msg2 = request.args.get('msg2', '')
               conn = get_db_connection()
               cur = conn.cursor()
               cur.execute(
    '''SELECT DISTINCT Program_ID FROM Programs''')
    
               prog = cur.fetchall()
  
  
        
               cur.execute('''SELECT Students.s_id, Students.First_Name, Students.Last_Name, COALESCE(Students.Program_ID, 'No Program'),COALESCE(Programs.Program_Name, 'No Program'), COALESCE(Students.student_image, 'No Image') FROM Students LEFT JOIN Programs ON Students.Program_ID = Programs.Program_ID ''', 
                   )
               items_on_page = cur.fetchall()
               return render_template("Student.html", items_on_page=items_on_page, prog=prog,msg2=msg2)
          except psycopg2.Error as e:
               conn.rollback()
               return f"Database error: {str(e)}", 400
          finally:
            cur.close()
            conn.close()

          
@student_bp.route('/s_create', methods=['POST'])
def create():
 conn = get_db_connection()

 cur = conn.cursor()
 try:
    
    msg2 = ''
   
    s_id = request.form['s_id']
    First_Name = request.form['First_Name']
    Last_Name = request.form['Last_Name']
    Program_ID = request.form['Program_ID']
    profpic_file = request.files.get("profilePictureUpload")

    if not s_id or not First_Name or not Last_Name or not Program_ID:
        msg2 =  "Required fields missing"
    else: cur.execute(
        '''INSERT INTO Students \
        (s_id, First_Name, Last_Name, Program_ID) VALUES (%s, %s, %s, %s)''',
        (s_id, First_Name, Last_Name, Program_ID))
    conn.commit()
    
    if profpic_file and profpic_file.filename:
        filename = secure_filename(profpic_file.filename)
        file_ext = os.path.splitext(filename)[1].lower() or '.png'
        ext_without_dot = file_ext[1:] if file_ext.startswith('.') else file_ext
        if ext_without_dot == 'jpeg':
            ext_without_dot = 'jpg'
        allowed_extensions = ['jpg', 'jpeg', 'png']
        if ext_without_dot not in allowed_extensions:
            flash("Invalid file type. Only image files (JPG, JPEG, PNG) are allowed.")
            cur.close()
            conn.close()
            return redirect(url_for('student_bp.Home')) 
        
        content_type = f"image/{ext_without_dot}"
        unique_filename = f"cover_{Program_ID}_{filename}"
        file_data = profpic_file.read()
        
        try:
            print(f"Uploading cover photo '{unique_filename}' to Supabase...")
            supabase.storage.from_(SUPABASE_BUCKET).upload(
                unique_filename,
                file_data,
                file_options={"content-type": content_type, "upsert": "true"}
            )
            prof_photo_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(unique_filename)
            print(f"Uploaded cover photo URL: {prof_photo_url}")
          
            query = '''UPDATE Students SET student_image = %s WHERE s_id = %s '''
            cur.execute(query
            ,
            (prof_photo_url, s_id))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error uploading cover photo: {e}")
            flash("Failed to upload cover photo.")

    

    return redirect(url_for('student_bp.Home', msg2=msg2)) 
 except psycopg2.Error as e:
               conn.rollback()
               msg2 = 'Error!, Invalid Form Applied.'
               return redirect(url_for('student_bp.Home', msg2=msg2)) 
 finally:
    cur.close()
    conn.close()

    


@student_bp.route('/s_update', methods=['POST'])
def update():
    conn =  conn = get_db_connection()

    cur = conn.cursor()
    s_id = request.form['s_id']
    First_Name = request.form['First_Name']
    Last_Name = request.form['Last_Name']
    Program_ID = request.form['Program_ID']
    profpic_file = request.files.get("profilePictureUpload")
    cur.execute(
        '''UPDATE Students SET First_Name=%s, \
        Last_Name=%s, Program_ID=%s WHERE s_id=%s ''', (First_Name, Last_Name, Program_ID, s_id ))
    if profpic_file and profpic_file.filename:
        filename = secure_filename(profpic_file.filename)
        file_ext = os.path.splitext(filename)[1].lower() or '.png'
        ext_without_dot = file_ext[1:] if file_ext.startswith('.') else file_ext
        if ext_without_dot == 'jpeg':
            ext_without_dot = 'jpg'
        allowed_extensions = ['jpg', 'jpeg', 'png']
        if ext_without_dot not in allowed_extensions:
            flash("Invalid file type. Only image files (JPG, JPEG, PNG) are allowed.")
            cur.close()
            conn.close()
            return redirect(url_for('student_bp.Home')) 
        
        content_type = f"image/{ext_without_dot}"
        unique_filename = f"cover_{Program_ID}_{filename}"
        file_data = profpic_file.read()
        
        try:
            print(f"Uploading cover photo '{unique_filename}' to Supabase...")
            supabase.storage.from_(SUPABASE_BUCKET).upload(
                unique_filename,
                file_data,
                file_options={"content-type": content_type, "upsert": "true"}
            )
            prof_photo_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(unique_filename)
            print(f"Uploaded cover photo URL: {prof_photo_url}")
          
            query = '''UPDATE Students SET student_image = %s WHERE s_id = %s '''
            cur.execute(query
            ,
            (prof_photo_url, s_id))
            
        except Exception as e:
            print(f"Error uploading cover photo: {e}")
            flash("Failed to upload cover photo.")

 

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('student_bp.Home') )


@student_bp.route('/s_delete', methods=['POST'])
def delete():
    conn =  conn = get_db_connection()
    cur = conn.cursor()


    s_id = request.form['s_id']

    cur.execute('''DELETE FROM Students WHERE s_id=%s''', (s_id,))

   
    conn.commit()

   
    cur.close()
    conn.close()
    return redirect(url_for('student_bp.Home'))