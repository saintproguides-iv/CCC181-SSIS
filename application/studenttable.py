from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras

student_bp = Blueprint('student_bp', __name__, template_folder="templates")

@student_bp.route('/Student')
def Home():
 if not session.get('loggedin'):
        
        return render_template("login.html")
 else:
          try:
               msg2 = request.args.get('msg2', '')
               conn = psycopg2.connect(database="flask_db",
                           user="postgres",
                           password="saint",
                           host="localhost", port="5432")
               cur = conn.cursor()
               cur.execute(
    '''SELECT DISTINCT Program_ID FROM Programs''')
    
               prog = cur.fetchall()
  
  
        
               cur.execute('''SELECT Students.s_id, Students.First_Name, Students.Last_Name, COALESCE(Students.Program_ID, 'No Program'),COALESCE(Programs.Program_Name, 'No Program') FROM Students LEFT JOIN Programs ON Students.Program_ID = Programs.Program_ID ''', 
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
 conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="saint",
                            host="localhost", port="5432")

 cur = conn.cursor()
 try:
    
    msg2 = ''
   
    s_id = request.form['s_id']
    First_Name = request.form['First_Name']
    Last_Name = request.form['Last_Name']
    Program_ID = request.form['Program_ID']

    if not s_id or not First_Name or not Last_Name or not Program_ID:
        msg2 =  "Required fields missing"
    else: cur.execute(
        '''INSERT INTO Students \
        (s_id, First_Name, Last_Name, Program_ID) VALUES (%s, %s, %s, %s)''',
        (s_id, First_Name, Last_Name, Program_ID))
    conn.commit()
    
    

    

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
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="saint",
                            host="localhost", port="5432")

    cur = conn.cursor()
    s_id = request.form['s_id']
    First_Name = request.form['First_Name']
    Last_Name = request.form['Last_Name']
    Program_ID = request.form['Program_ID']


    cur.execute(
        '''UPDATE Students SET First_Name=%s, \
        Last_Name=%s, Program_ID=%s WHERE s_id=%s ''', (First_Name, Last_Name, Program_ID, s_id ))
 

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('student_bp.Home') )


@student_bp.route('/s_delete', methods=['POST'])
def delete():
    conn = psycopg2.connect (database="flask_db", user="postgres", password="saint", host="localhost", port="5432")
    cur = conn.cursor()


    s_id = request.form['s_id']

    cur.execute('''DELETE FROM Students WHERE s_id=%s''', (s_id,))

   
    conn.commit()

   
    cur.close()
    conn.close()
    return redirect(url_for('student_bp.Home'))