from flask import Flask



import os
from app.student.studenttable import student_bp
from app.program.programtable import program_bp
from app.college.collegetable import college_bp
from app.login.loginpath import loginpath

BASE_DIR = os.path.dirname(os.path.abspath(__file__))




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