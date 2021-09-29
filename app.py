from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/another')
def second():
    return render_template('another.html')

app.debug =  True
app.run()