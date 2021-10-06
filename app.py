import sqlite3
from flask import Flask,render_template,request,url_for
import os

app = Flask(__name__, static_folder='./static')

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

    cursor.execute("select title, sport, content from post where sport like ?",(search_name,))
    search_result = cursor.fetchall()

    if search_result ==[]:
        print("該当なし")
        return render_template("index.html",search_result=search_result)
        #HTML上にアラートとして出力
    else:
        return render_template("index.html",search_result=search_result)
        print("ui")
    cursor.close()

    # # タイトルを出力
    # cursor.execute("select title from post where sport like ?",(search_name,))
    # title_result = cursor.fetchall()

    # # スポーツを出力
    # cursor.execute("select sport from post where sport like ?",(search_name,))
    # sport_result = cursor.fetchall()

    # #　コンテンツを出力
    # cursor.execute("select content from post where sport like ?",(search_name,))
    # contents_result = cursor.fetchall()
   
    # if title_result and sport_result and contents_result ==[]:
    #     print("該当なし")
    #     return render_template("index.html",title_name = title_result, sport_name = sport_result, contents_name = contents_result)
    #     #HTML上にアラートとして出力
    # else:
    #     return render_template("index.html",title_name = title_result, sport_name = sport_result, contents_name = contents_result)
    #     print("ui")
    # cursor.close()

db_conect.commit()
# cursor.close()
db_conect.commit()

app.debug =  True
app.run()

#cssが更新されてもwebにキャッシュされる不具合を解消するコード
#また、このコードを追記するにあたってos,url_forをimportした
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
    #ここまで