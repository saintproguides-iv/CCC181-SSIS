from flask import Flask, redirect, url_for, render_template


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("Home.html")


@app.route("/College")
def College():
    return render_template("College.html")

@app.route("/Student")
def Home():
    return render_template("Student.html")

@app.route("/Programs")
def Program():
    return render_template("Programs.html")



if __name__ == "__main__":
    app.run(debug=True)