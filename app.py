from flask import Flask, render_template
import requests
import json

from bookstore import Bookstore, Book

app = Flask(__name__)
bookstore = Bookstore()

@app.route('/')
def index():
    bookstore.fetch()
    return render_template("index.html", books = bookstore.books, magazines = bookstore.magazines)

@app.route('/dashboard')
def dashboard():
    return "dashboard"

@app.route('/data/books')
def books():
    f = open("data/books.json")
    data = json.load(f)
    return data

@app.route('/data/magazines')
def magazines():
    f = open("data/magazines.json")
    data = json.load(f)
    return data
