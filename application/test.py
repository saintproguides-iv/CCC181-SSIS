from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import psycopg2
import os
from models.loginmodel import registerquery, loginquery
from studenttable import student_bp
from programtable import program_bp
from collegetable import college_bp
from loginpath import loginpath
login_manager = LoginManager()

app = Flask(__name__)
app.register_blueprint(loginpath, url_prefix="")
app.register_blueprint(student_bp, url_prefix="")
app.register_blueprint(program_bp, url_prefix="")
app.register_blueprint(college_bp, url_prefix="")
app.config["SESSION_PERMANENT"] = False 
app.secret_key = os.getenv("SECRET_KEY")

    



    
if __name__ == "__main__":
    app.run(debug=True)