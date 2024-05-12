from flask import Flask, render_template
import requests
import json

from items import Book

app = Flask(__name__)

@app.route('/')
def index():
    res = requests.get("http://127.0.0.1:5000/data/books")
    data = res.json()

    books = []

    for item in data:
        book = Book(item["title"], item["author"], item["price"], item["ISBN"], item["genre"], item["pages"])
        books.append(book)

    return render_template("index.html", books = books)

@app.route('/dashboard')
def dashboard():
    return "dashboard"

@app.route('/data/books')
def books():
    f = open("books.json")
    data = json.load(f)
    return data
