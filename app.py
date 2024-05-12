from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    res = requests.get("http://127.0.0.1:5000/data/books")
    books = res.json()
    return render_template("index.html", books = books)

@app.route('/data/books')
def books():
    f = open("books.json")
    data = json.load(f)
    return data
