import sqlite3
from flask import Flask,render_template

app = Flask(__name__, static_folder='./templates/images')
db_conect = sqlite3.connect("texpo.db")
cursor = db_conect.cursor()


@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/another')
def second():
    return render_template('another.html')

@app.route('/upload', methods=["GET", "POST"])
def upload():
    cursor.execute = ("INSERT INTO post (title, sport, content) VALUES (?, ?, ?)",
                  request.form.get("title"), request.form.get("sport"), request.form.get("content"))
    return redirect("/")

app.debug =  True
app.run()

# Hello world