import sqlite3
from flask import Flask,render_template,request

app = Flask(__name__, static_folder='./templates/images')

db_conect = sqlite3.connect("texpo.db", check_same_thread=False)
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

@app.route("/search")
def search():
    return render_template("search.html")

    
@app.route("/search_pattern", methods=["POST"])
def search_pattern():
    search_name  = request.form["Sport"]
    cursor.execute("select sport from post where sport like ?",(search_name,))
    search_result = cursor.fetchall()

    if search_result ==[]:
        print("該当なし")
        return render_template("index.html",sport_name = search_result)
        #HTML上にアラートとして出力
    else:
        return render_template("index.html",sport_name = search_result)
        print("ui")
    cursor.close()

db_conect.commit()
# cursor.close()
db_conect.commit()

app.debug =  True
app.run()

# Hello world

#編集