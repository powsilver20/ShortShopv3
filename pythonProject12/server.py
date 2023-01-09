
from flask import Flask, request, redirect, url_for , render_template

app = Flask(__name__)
import sqlite3

@app.route('/')
def test():
    return redirect("/create")

@app.route('/create')
def createlisting():
    return render_template('index.html')

@app.route('/yourlistings')
def yourlistings():
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True)

