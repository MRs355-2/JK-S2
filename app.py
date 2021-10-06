import sqlite3
from flask import Flask,render_template
app = Flask(__name__)
conn = sqlite3.connect('texpo.db') 
c = conn.cursor() 


@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/another', methods=["GET", "POST"])
def second(): 
    cursor.execute = ("INSERT INTO post (title, sport, content) VALUES (?, ?, ?)",
                  request.form.get("title"), request.form.get("sport"), request.form.get("content"))
    return render_template('another.html')

@app.route('/upload', methods=["GET", "POST"])
def upload():
<<<<<<< Updated upstream
    c.execute = ("INSERT INTO post (title, sport, content) VALUES (?, ?, ?)", 
                  request.form.get("title"), request.form.get("sport"), request.form.get("content"))
=======
>>>>>>> Stashed changes
    return redirect("/")

app.debug =  True
app.run()