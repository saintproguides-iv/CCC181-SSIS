from flask import Flask,Blueprint, flash, g, redirect, url_for, render_template, request, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import psycopg2, psycopg2.extras
import psycopg2
from studenttable import student_bp
from programtable import program_bp
from collegetable import college_bp
login_manager = LoginManager()

app = Flask(__name__)
app.register_blueprint(student_bp, url_prefix="")
app.register_blueprint(program_bp, url_prefix="")
app.register_blueprint(college_bp, url_prefix="")
app.config["SESSION_PERMANENT"] = False 
app.secret_key = 'gsegwsegasefqwe344qwe'

    


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        conn = psycopg2.connect(database="flask_db",
                               user="postgres",
                               password="saint",
                               host="localhost", port="5432")

        cur = conn.cursor()
        user_id = request.form['user_id']
        username = request.form['Username']
        user_password = request.form['user_password'] 
        actual_pass = generate_password_hash(user_password, method='pbkdf2:sha256')
        
        try:
            # Check if user_id already exists
            cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            existing_user = cur.fetchone()
            
            if existing_user:
                msg = 'User ID already exists. Please choose a different one.'
            else:
                cur.execute(
                    '''INSERT INTO users \
                    (user_id, username, user_password) VALUES (%s,%s, %s)''',
                    (user_id, username, actual_pass))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('login'))
                
        except psycopg2.IntegrityError:
            msg = 'User ID already exists. Please choose a different one.'
        except Exception as e:
            msg = f'An error occurred: {str(e)}'
        finally:
            cur.close()
            conn.close()
    
    return render_template("register.html", msg=msg)
@app.route("/Home")
def Homepage():
    return render_template("Home.html")
@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = psycopg2.connect(database="flask_db",
                            user="postgres",
                            password="saint",
                            host="localhost", port="5432")
    cur = conn.cursor()

    msg = ''
    if request.method == 'POST' and 'user_id' in request.form and 'username' in request.form and 'password' in request.form:
        user_id = request.form['user_id']
        username = request.form['username']
        password = request.form['password']
        
        cur.execute('SELECT * FROM users WHERE user_id = %s AND username = %s', (user_id, username))
        account = cur.fetchone()
        cur.execute('SELECT user_password FROM users WHERE user_id = %s AND username = %s', (user_id, username))
        hashpass = cur.fetchone()
        if account and check_password_hash(hashpass[0], password):
         print("step works")
         print(account[0])
         session['loggedin'] = True
         session['id'] = account[0]
         session['username'] = account[1]
         return redirect(url_for('Homepage'))
         
           
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)
    








        


if __name__ == "__main__":
    app.run(debug=True)