from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
import os
from supabase import create_client
from werkzeug.utils import secure_filename
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "uploads")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
)
    return conn
def base_students():
     msg2 = request.args.get('msg2', '')
     conn = get_db_connection()
     cur = conn.cursor()
     cur.execute("SELECT DISTINCT Program_ID FROM Programs")
     prog = cur.fetchall()
     cur.close()
     conn.close()
     return prog, msg2
 

def get_students(start, length, search_value, order_column, order_dir):
    conn = get_db_connection()
    
    cur = conn.cursor()

    base_query = '''
        SELECT s_id, First_Name, Last_Name,
               COALESCE(Students.Program_ID, 'No Program'),
               COALESCE(Programs.Program_Name, 'No Program'),
               COALESCE(Students.student_image, 'No Image'),
               COALESCE(Students.year_level, 'No Year Level'),
               COALESCE(Students.gender, 'No Gender')
        FROM Students
        LEFT JOIN Programs ON Students.Program_ID = Programs.Program_ID
    '''
    params = []

    if search_value:
        base_query += " WHERE First_Name ILIKE %s OR Last_Name ILIKE %s OR (First_Name || ' ' || Last_Name) ILIKE %s OR Students.Program_ID ILIKE %s OR s_id ILIKE %s"
        params.extend([f"%{search_value}%", f"%{search_value}%", f"%{search_value}%",f"%{search_value}%",f"%{search_value}%"])

    base_query += f" ORDER BY {order_column} {order_dir.upper()} LIMIT %s OFFSET %s"
    params.extend([length, start])

    cur.execute(base_query, tuple(params))
    data = cur.fetchall()

  
    cur.execute("SELECT COUNT(*) FROM Students")
    records_total = cur.fetchone()[0]

    if search_value:
        cur.execute("SELECT COUNT(*) FROM Students WHERE First_Name ILIKE %s OR Last_Name ILIKE %s OR (First_Name || ' ' || Last_Name) ILIKE %s OR  Students.Program_ID ILIKE %s OR s_id ILIKE %s",
                    (f"%{search_value}%", f"%{search_value}%", f"%{search_value}%", f"%{search_value}%",f"%{search_value}%"))
        records_filtered = cur.fetchone()[0]
    else:
        records_filtered = records_total

    cur.close()
    conn.close()

    return data, records_total, records_filtered

def creates(s_id, First_Name, Last_Name,Program_ID,Gender,Year_Level,profpic_file):
 conn = get_db_connection()

 cur = conn.cursor()
 try:
    msg2 = ''
    

    if not s_id or not First_Name or not Last_Name or not Program_ID:
        msg2 =  "Required fields missing"
    else: cur.execute(
        '''INSERT INTO Students \
        (s_id, First_Name, Last_Name, Program_ID, Gender, year_level) VALUES (%s, %s, %s, %s,%s,%s)''',
        (s_id, First_Name, Last_Name, Program_ID, Gender, Year_Level))
    conn.commit()
    
    if profpic_file and profpic_file.filename:
        filename = secure_filename(profpic_file.filename)
        file_ext = os.path.splitext(filename)[1].lower() or '.png'
        ext_without_dot = file_ext[1:] if file_ext.startswith('.') else file_ext
        if ext_without_dot == 'jpeg':
            ext_without_dot = 'jpg'
        allowed_extensions = ['jpg', 'jpeg', 'png']
        if ext_without_dot not in allowed_extensions:
            msg2 = f'Invalid file type. Only image files (JPG, JPEG, PNG) are allowed. Giving default picture instead.'
            cur.close()
            conn.close()
            return msg2
        
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

    

    return msg2
 except psycopg2.Error as e:
               conn.rollback()
               msg2 = f'ID is invalid, did not insert student'
               return  msg2
 finally:
    cur.close()
    conn.close()
    
def updates(s_id, First_Name, Last_Name,Program_ID,Gender,Year_Level,profpic_file):
    conn =  conn = get_db_connection()

    cur = conn.cursor()
    
    cur.execute(
        '''UPDATE Students SET First_Name=%s, \
        Last_Name=%s, Program_ID=%s, Gender=%s, year_level=%s WHERE s_id=%s ''', (First_Name, Last_Name, Program_ID,Gender,Year_Level, s_id ))
    if profpic_file and profpic_file.filename:
        filename = secure_filename(profpic_file.filename)
        file_ext = os.path.splitext(filename)[1].lower() or '.png'
        ext_without_dot = file_ext[1:] if file_ext.startswith('.') else file_ext
        if ext_without_dot == 'jpeg':
            ext_without_dot = 'jpg'
        allowed_extensions = ['jpg', 'jpeg', 'png']
        if ext_without_dot not in allowed_extensions:
            print("invalid")
            msg2 = f'Invalid file type. Only image files (JPG, JPEG, PNG) are allowed.'
            cur.close()
            conn.close()
            return msg2 
        
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
   
def deletes(s_id):
    conn =  conn = get_db_connection()
    cur = conn.cursor()


    

    cur.execute('''DELETE FROM Students WHERE s_id=%s''', (s_id,))

   
    conn.commit()

   
    cur.close()
    conn.close()
   