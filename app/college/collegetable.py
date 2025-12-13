from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
import psycopg2, psycopg2.extras
from app.models.cmodel import get_colleges, ccreate, cupdate,cdelete
college_bp = Blueprint('college_bp', __name__, template_folder="../templates")

@college_bp.route('/College')
def Home():
 

               
 if not session.get('loggedin'):
        
        return render_template("login.html")
 else: 
          items_on_page, msg2 = get_colleges()
          return render_template("College.html", items_on_page=items_on_page,msg2=msg2 )
            
@college_bp.route('/c_create', methods=['POST'])
def create():
    print("CREATE ROUTE HIT!") 
    
       
    college_id = request.form['college_id']
    college_name = request.form['college_name']
    msg2 =  ccreate(college_id, college_name)
    return redirect(url_for('college_bp.Home', msg2=msg2)) 
    

    


@college_bp.route('/c_update', methods=['POST'])
def update():
    college_id = request.form['college_id']
    college_name = request.form['college_name']
    cupdate(college_name, college_id)
    return redirect(url_for('college_bp.Home')) 


@college_bp.route('/c_delete', methods=['POST'])
def delete():
    
   


    college_id = request.form['college_id']

    
    cdelete(college_id)
    return redirect(url_for('college_bp.Home')) 