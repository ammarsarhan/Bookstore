from flask import Flask, render_template, request, redirect
import requests
import json

from bookstore import Bookstore, Book

app = Flask(__name__)
bookstore = Bookstore()

@app.route('/')
def index():
    bookstore.fetchAll()
    return render_template("index.html", books = bookstore.books, magazines = bookstore.magazines)

@app.route('/update/book/<id>', methods=['GET', 'POST'])
def updateBook(id):
    if request.method == 'GET':
        book = bookstore.fetchItem("book", id)
        return render_template("update.html", type = "Book", id = id, item = book)
    elif request.method == 'POST':
        data = request.form
        bookstore.updateItem("book", id, data)
        return redirect("/")

@app.route('/update/magazine/<id>')
def updateMagazine(id):
    magazine = bookstore.fetchItem("magazine", id)
    return render_template("update.html", type = "Magazine", id = id, item = magazine)

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
