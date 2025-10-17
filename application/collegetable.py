from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
college_bp = Blueprint('college_bp', __name__, template_folder="templates")

@college_bp.route('/College')
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
              
             
  
        
               cur.execute('''SELECT * FROM colleges''', 
                   )
               items_on_page = cur.fetchall()
               return render_template("College.html", items_on_page=items_on_page,msg2=msg2 )
          except psycopg2.Error as e:
               conn.rollback()
               return f"Database error: {str(e)}", 400
          finally:
            cur.close()
            conn.close()
            
@college_bp.route('/c_create', methods=['POST'])
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
       
        college_id = request.form['college_id']
        college_name = request.form['college_name']
        print({college_name, college_id})
        if not college_id or not college_name:
          msg2 = "Required fields missing"
        else:
            cur.execute(
            '''INSERT INTO colleges (college_id, college_name) VALUES (%s, %s)''',
            (college_id, college_name))
        conn.commit()
        print("Insert successful!")
        
        return redirect(url_for('college_bp.Home', msg2=msg2)) 
     
    except psycopg2.Error as e:
        print(f"DATABASE ERROR: {e}")  
        if conn:  
            conn.rollback()
        msg2 = f'Error! {e}'  
        return redirect(url_for('college_bp.Home', msg2=msg2)) 
    
    except Exception as e:
        print(f"GENERAL ERROR: {e}")  # CATCH OTHER ERRORS
        if conn:
            conn.rollback()
        msg2 = f'Error! {e}'
        return redirect(url_for('college_bp.Home', msg2=msg2))
    
    finally:
        if cur:  # CHECK IF cur EXISTS BEFORE CLOSING
            cur.close()
        if conn:  # CHECK IF conn EXISTS BEFORE CLOSING
            conn.close()

    


@college_bp.route('/c_update', methods=['POST'])
def update():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="saint",
                            host="localhost", port="5432")

    cur = conn.cursor()
    college_id = request.form['college_id']
    college_name = request.form['college_name']


    cur.execute(
        '''UPDATE colleges SET college_name=%s WHERE college_id=%s ''', (college_name, college_id ))
 

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('college_bp.Home') )


@college_bp.route('/c_delete', methods=['POST'])
def delete():
    conn = psycopg2.connect (database="flask_db", user="postgres", password="saint", host="localhost", port="5432")
    cur = conn.cursor()


    college_id = request.form['college_id']

    cur.execute('''DELETE FROM colleges WHERE college_id=%s''', (college_id, ))

   
    conn.commit()

   
    cur.close()
    conn.close()
    return redirect(url_for('college_bp.Home'))