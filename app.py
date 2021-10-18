import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
from contextlib import closing
import socket

app = Flask(__name__, static_folder='./static')

db_connect = sqlite3.connect("texpo.db", check_same_thread=False)
cursor = db_connect.cursor()

#ここで選択できるスポーツを追加
sports_name = ["サッカー", "テニス", "ゴルフ", "バレー"]

user_host = socket.gethostname()
user_ip = socket.gethostbyname(user_host)

@app.route("/")
def search():
    print(user_ip)
    return render_template("search.html")

    
@app.route("/search_pattern", methods=["GET","POST"])
def search_pattern():
    search_name = request.form["Sport"]
    sort_result = request.form.get("sort")

    if search_name == "":
        return render_template("search.html")

    else:
        if sort_result == "id":
            cursor.execute("select title, sport, content, id from post where sport like ? order by id desc;",(search_name,))
            search_result = cursor.fetchall()
        elif sort_result == "like":
            cursor.execute("select title, sport, content, id from post where sport like ? order by like desc;",(search_name,))
            search_result = cursor.fetchall()
        else:
            cursor.execute("select title, sport, content, id from post where sport like ?",(search_name,))
            search_result = cursor.fetchall()

    if search_result ==[]:

        if sort_result == "id":
            cursor.execute("select title, sport, content, id from post where title like ? order by id desc;",("%"+ search_name +"%",))
            search_result = cursor.fetchall()
        elif sort_result == "like":
            cursor.execute("select title, sport, content, id from post where title like ? order by like desc;",("%"+ search_name +"%",))
            search_result = cursor.fetchall()
        else:
            cursor.execute("select title, sport, content, id from post where title like ?",("%"+ search_name +"%",))
            search_result = cursor.fetchall()

        if search_result ==[]:
            notfound = "検索結果が見つかりませんでした。"
            return render_template("search.html", notfound=notfound)
        else:
            return render_template("search.html",search_result=search_result)
    else:
            return render_template("search.html",search_result=search_result)

    cursor.close()

    
@app.route('/another', methods=["GET", "POST"])
def second():
    return render_template('another.html', sports_name=sports_name)

@app.route('/upload', methods=["GET", "POST"])
def upload():
    cursor.execute("INSERT INTO post (title, sport, content) VALUES (?, ?, ?)",
                  [request.form.get("title"), request.form.get("sport"), request.form.get("content")])
                  
    return redirect("/")

db_connect.commit()
# cursor.close()


#####テスト#####


#####テスト#####

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