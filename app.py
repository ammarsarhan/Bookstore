from flask import Flask, render_template, request, redirect
import json

from bookstore import Bookstore, Book, Magazine, DVD

app = Flask(__name__)
bookstore = Bookstore()

# Home
@app.route('/')
def index():
    bookstore.fetchAll()
    return render_template("index.html", books = bookstore.books, magazines = bookstore.magazines, dvds = bookstore.dvds,
                           bookIndex = len(bookstore.books) + 1, magazineIndex = len(bookstore.magazines) + 1, dvdIndex = len(bookstore.dvds) + 1)

@app.route('/add/book/<id>', methods=['GET', 'POST'])
def addBook(id):
    if request.method == 'GET':
        return render_template("add.html", type = "Book", id = id)
    else:
        data = request.form
        bookstore.addItem("book", id, data)
        return redirect("/")

@app.route('/add/magazine/<id>', methods=['GET', 'POST'])
def addMagazine(id):
    if request.method == 'GET':
        return render_template("add.html", type = "Magazine", id = id)
    else:
        data = request.form
        bookstore.addItem("magazine", id, data)
        return redirect("/")

@app.route('/add/dvd/<id>', methods=['GET', 'POST'])
def addDVD(id):
    if request.method == 'GET':
        return render_template("add.html", type = "DVD", id = id)
    else:
        data = request.form
        bookstore.addItem("dvd", id, data)
        return redirect("/")

# Search
@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template("search.html")
    else:
        args = {"title": request.form.get("title"), "author": request.form.get("author"), "price": request.form.get("price"), "operator": request.form.get("operator")}
        data = bookstore.searchItems(args)
        results = []

        for item in data:
            results.append(item.getData())
        
        f = open("data/results.json", "w")
        json.dump(results, f)

        return redirect('/search/display')
    
@app.route('/search/display')
def display():
    f = open("data/results.json", "r")
    data = json.load(f)
    return render_template("display.html", data = data)

# Dashboard
@app.route("/dashboard")
def dashboard():
    orders = bookstore.orders
    bill = round(bookstore.bill, 2) + 0

    return render_template("dashboard.html", orders = enumerate(orders), bill = bill)

@app.route("/remove/<id>")
def removeOrder(id):
    item = bookstore.orders[int(id) - 1].getData()
    price = float(item["price"])
    bookstore.bill = bookstore.bill - price + 0

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
    
@app.route('/update/dvd/<id>', methods=['GET', 'POST'])
def updateDVD(id):
    if request.method == 'GET':
        dvd = bookstore.fetchItem("dvd", id)
        return render_template("update.html", type = "DVD", id = id, item = dvd)
    elif request.method == 'POST':
        data = request.form
        bookstore.updateItem("dvd", id, data)
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
        bookstore.bill = bookstore.bill + float(data["price"]) + 0
        
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
        bookstore.bill = bookstore.bill + float(data["price"]) + 0
        
        return redirect("/")

@app.route('/order/dvd/<id>', methods=['GET', 'POST'])
def orderDVD(id):
    if request.method == 'GET':
        dvd = bookstore.fetchItem("dvd", id)
        return render_template("order.html", type = "DVD", id = id, item = dvd)
    elif request.method == 'POST':
        data = bookstore.fetchItem("dvd", id)
        dvd = DVD(data["title"], data["author"], data["price"], data["director"], data["duration"], data["genre"])

        bookstore.orders.append(dvd)
        bookstore.bill = bookstore.bill + float(data["price"]) + 0
        
        return redirect("/")

# JSON Data Requests
@app.route('/data/books')
def books():
    f = open("data/books.json", "r")
    data = json.load(f)
    return data

@app.route('/data/magazines')
def magazines():
    f = open("data/magazines.json", "r")
    data = json.load(f)
    return data

@app.route('/data/dvds')
def dvds():
    f = open("data/dvds.json", "r")
    data = json.load(f)
    return data
