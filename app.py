from flask import Flask, render_template, request, redirect
import json

from bookstore import Bookstore, Book, Magazine

app = Flask(__name__)
bookstore = Bookstore()

# Home
@app.route('/')
def index():
    bookstore.fetchAll()
    return render_template("index.html", books = bookstore.books, magazines = bookstore.magazines)

# Search
@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template("search.html")

# Dashboard
@app.route("/dashboard")
def dashboard():
    orders = bookstore.orders
    bill = round(bookstore.bill, 2)

    return render_template("dashboard.html", orders = enumerate(orders), bill = bill)

@app.route("/remove/<id>")
def removeOrder(id):
    item = bookstore.orders[int(id) - 1].getData()
    price = float(item["price"])
    bookstore.bill = bookstore.bill - price

    bookstore.orders.pop(int(id) - 1)

    return redirect("/dashboard")

# Bookstore Update Routes
@app.route('/update/book/<id>', methods=['GET', 'POST'])
def updateBook(id):
    if request.method == 'GET':
        book = bookstore.fetchItem("book", id)
        return render_template("update.html", type = "Book", id = id, item = book)
    elif request.method == 'POST':
        data = request.form
        bookstore.updateItem("book", id, data)
        return redirect("/")

@app.route('/update/magazine/<id>', methods=['GET', 'POST'])
def updateMagazine(id):
    if request.method == 'GET':
        magazine = bookstore.fetchItem("magazine", id)
        return render_template("update.html", type = "Magazine", id = id, item = magazine)
    elif request.method == 'POST':
        data = request.form
        bookstore.updateItem("magazine", id, data)
        return redirect("/")

# Bookstore Order Routes
@app.route('/order/book/<id>', methods=['GET', 'POST'])
def orderBook(id):
    if request.method == 'GET':
        book = bookstore.fetchItem("book", id)
        return render_template("order.html", type = "Book", id = id, item = book)
    elif request.method == 'POST':
        data = bookstore.fetchItem("book", id)
        book = Book(data["title"], data["author"], data["price"], data["ISBN"], data["genre"], data["pages"])

        bookstore.orders.append(book)
        bookstore.bill = bookstore.bill + float(data["price"])
        
        return redirect("/")

@app.route('/order/magazine/<id>', methods=['GET', 'POST'])
def orderMagazine(id):
    if request.method == 'GET':
        magazine = bookstore.fetchItem("magazine", id)
        return render_template("order.html", type = "Magazine", id = id, item = magazine)
    elif request.method == 'POST':
        data = bookstore.fetchItem("magazine", id)
        magazine = Magazine(data["title"], data["author"], data["price"], data["issue"], data["publication"], data["editor"])

        bookstore.orders.append(magazine)
        bookstore.bill = bookstore.bill + float(data["price"])
        
        return redirect("/")

# JSON Data Requests
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
