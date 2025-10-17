from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
program_bp = Blueprint('program_bp', __name__, template_folder="templates")

@program_bp.route('/Programs')
def Home():
 conn = psycopg2.connect(database="flask_db",
                           user="postgres",
                           password="saint",
                           host="localhost", port="5432")
 cur = conn.cursor()

               
 if not session.get('loggedin'):
        
        return render_template("login.html")
 else: 
          try:
               msg2 = request.args.get('msg2', '')
              
               cur.execute(
    '''SELECT DISTINCT College_ID FROM colleges''')
    
               clg = cur.fetchall()
  
        
               cur.execute('''SELECT program_id, program_name, COALESCE(college_in, 'No College') FROM programs''', 
                   )
               items_on_page = cur.fetchall()
               return render_template("Programs.html", items_on_page=items_on_page,msg2=msg2,clg=clg )
          except psycopg2.Error as e:
               conn.rollback()
               return f"Database error: {str(e)}", 400
          finally:
            cur.close()
            conn.close()
            
@program_bp.route('/p_create', methods=['POST'])
def create():
    print("CREATE ROUTE HIT!") 
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(database="flask_db",
                                user="postgres",
                                password="saint",
                                host="localhost", port="5432")

        cur = conn.cursor()
        msg2 = ''
       
        program_id = request.form['program_id']
        program_name = request.form['program_name']
        college_in = request.form['college_in']
        if not program_id or not program_name or not college_in:
          msg2 = "Required fields missing"
        else:
            cur.execute(
            '''INSERT INTO programs (program_id, program_name, college_in) VALUES (%s, %s, %s)''',
            (program_id, program_name, college_in))
        conn.commit()
        print("Insert successful!")
        
        return redirect(url_for('program_bp.Home', msg2=msg2)) 
     
    except psycopg2.Error as e:
        print(f"DATABASE ERROR: {e}")  
        if conn:  
            conn.rollback()
        msg2 = f'Error! {e}'  
        return redirect(url_for('program_bp.Home', msg2=msg2)) 
    
    except Exception as e:
        print(f"GENERAL ERROR: {e}")  # CATCH OTHER ERRORS
        if conn:
            conn.rollback()
        msg2 = f'Error! {e}'
        return redirect(url_for('program_bp.Home', msg2=msg2))
    
    finally:
        if cur:  # CHECK IF cur EXISTS BEFORE CLOSING
            cur.close()
        if conn:  # CHECK IF conn EXISTS BEFORE CLOSING
            conn.close()

    


@program_bp.route('/p_update', methods=['POST'])
def update():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="saint",
                            host="localhost", port="5432")

    cur = conn.cursor()
    program_id = request.form['program_id']
    program_name = request.form['program_name']
    college_in = request.form['college_in']
   


    cur.execute(
        '''UPDATE programs SET program_name=%s, \
         college_in=%s WHERE program_id=%s ''', (program_name, college_in, program_id ))
 

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('program_bp.Home') )


@program_bp.route('/p_delete', methods=['POST'])
def delete():
    conn = psycopg2.connect (database="flask_db", user="postgres", password="saint", host="localhost", port="5432")
    cur = conn.cursor()


    program_id = request.form['program_id']

    cur.execute('''DELETE FROM programs WHERE program_id=%s''', (program_id,))

   
    conn.commit()

   
    cur.close()
    conn.close()
    return redirect(url_for('program_bp.Home'))