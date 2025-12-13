from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import psycopg2
import os
from app.models.loginmodel import registerquery, loginquery
from app.student.studenttable import student_bp
from app.program.programtable import program_bp
from app.college.collegetable import college_bp
from app.login.loginpath import loginpath

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
login_manager = LoginManager()



app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "app", "static"),
    template_folder=os.path.join(BASE_DIR, "app", "templates"),)
app.register_blueprint(loginpath, url_prefix="")
app.register_blueprint(student_bp, url_prefix="")
app.register_blueprint(program_bp, url_prefix="")
app.register_blueprint(college_bp, url_prefix="")
app.config["SESSION_PERMANENT"] = False 
app.secret_key = os.getenv("SECRET_KEY")

    



    
if __name__ == "__main__":
    app.run(debug=True)