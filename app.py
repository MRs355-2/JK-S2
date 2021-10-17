import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for
from contextlib import closing


app = Flask(__name__, static_folder='./static')

db_connect = sqlite3.connect("texpo.db", check_same_thread=False)
cursor = db_connect.cursor()

#ここで選択できるスポーツを追加
sports_name = ["サッカー", "テニス", "ゴルフ", "バレー"]


@app.route("/")
def search():
    return render_template("search.html")


@app.route("/search_pattern", methods=["POST"])
def search_pattern():

    search_name = request.form["Sport"]
    cursor.execute("select title, sport, content, id, likes from post where sport like ?",(search_name,))
    search_result = cursor.fetchall()
    if search_result ==[]:
        notfound = "検索結果が見つかりませんでした。"
        return render_template("search.html", notfound=notfound)
    else:
        return render_template("search.html",search_result=search_result, search_name=search_name)

    cursor.close()

@app.route('/another', methods=["GET", "POST"])
def second():
    return render_template('another.html', sports_name=sports_name)

@app.route('/upload', methods=["GET", "POST"])
def upload():
    cursor.execute("INSERT INTO post (title, sport, content) VALUES (?, ?, ?)",
                  [request.form.get("title"), request.form.get("sport"), request.form.get("content")])

    return redirect("/")

@app.route('/like', methods=["GET", "POST"])
def like():
    
    #like数を一つ増やす
    cursor.execute("select likes from post where id = ?", (request.form.get("like"),))
    likesplus = cursor.fetchall()
    likesplus = likesplus[0][0] + 1
    cursor.execute("UPDATE post SET likes = ? WHERE id = ?", (likesplus, request.form.get("like")))
    db_connect.commit()
    
    #ここで以前検索したページの情報を取りたいんですけど、このsearch_nameをどうやって取得するのかがわかりません
    #cursor.execute("select title, sport, content, id, likes from post where sport like ?",(search_name,))
    #search_result = cursor.fetchall()
    
    #likedはsearch.htmlでif文を使うために設定しました。とくに関係ありません。post_idはそのidの投稿に飛べるようにと思ったんですが、まだhtmlではなにもしていません。
    #return render_template("search.html",search_result=search_result, liked=True, post_id=request.form.get("like"))
    
    #とりあえず最初の検索画面に飛べるようにします
    return redirect("/")

db_connect.commit()
# cursor.close()



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