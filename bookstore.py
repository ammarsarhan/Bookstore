from abc import ABC, abstractmethod
import json
import requests

class Item(ABC):
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    @abstractmethod
    def getData(self):
        pass

    @abstractmethod
    def setData(self):
        pass

class Book(Item):
    def __init__(self, title, author, price, ISBN, genre, pages):
        super().__init__(title, author, price)
        self.ISBN = ISBN
        self.genre = genre
        self.pages = pages

    def getData(self):
        return {
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "ISBN": self.ISBN,
            "genre": self.genre,
            "pages": self.pages
        }
    
    def setData(self, attribute, value):
        match attribute:
            case "title":
                self.title = value
            case "author":
                self.author = value
            case "price":
                self.price = value
            case "ISBN":
                self.ISBN = value
            case "genre":
                self.genre = value
            case "pages":
                self.pages = value

        print(f"Updated {attribute} to {value}.")

class Magazine(Item):
    def __init__(self, title, author, price, issue, publication, editor):
        super().__init__(title, author, price)
        self.issue = issue
        self.publication = publication
        self.editor = editor

    def getData(self):
        return {
            "title": self.title,
            "author": self.author,
            "price": self.price,
            "issue": self.issue,
            "publication": self.publication,
            "editor": self.editor
        }
    
    def setData(self, attribute, value):
        match attribute:
            case "title":
                self.title = value
            case "author":
                self.author = value
            case "price":
                self.price = value
            case "issue":
                self.issue = value
            case "publication":
                self.publication = value
            case "editor":
                self.editor = value

        print(f"Updated {attribute} to {value}.")

class Bookstore:
    def __init__(self):
        self.books = []
        self.magazines = []
        self.orders = []
        self.bill = 0

    def fetchAll(self):
        self.books = []
        self.magazines = []

        res = requests.get("http://127.0.0.1:5000/data/books")
        data = res.json()

        for item in data:
            book = Book(item["title"], item["author"], item["price"], item["ISBN"], item["genre"], item["pages"])
            self.books.append(book)
        
        res = requests.get("http://127.0.0.1:5000/data/magazines")
        data = res.json()

        for item in data:
            magazine = Magazine(item["title"], item["author"], item["price"], item["issue"], item["publication"], item["editor"])
            self.magazines.append(magazine)

    def fetchItem(self, type, id):
        url = "http://127.0.0.1:5000/data/books" if (type == "book") else "http://127.0.0.1:5000/data/magazines"
     
        res = requests.get(url)
        data = res.json()

        return data[int(id) - 1]
    
    def updateItem(self, type, id, data):
        url = "http://127.0.0.1:5000/data/books" if (type == "book") else "http://127.0.0.1:5000/data/magazines" 
        
        res = requests.get(url)
        raw = res.json()

        # Figure out a way to do this (not locally)
        file = open("data/books.json", "w") if (type == "book") else open("data/magazines.json", "w")

        raw[int(id) - 1] = data
        json.dump(raw, file)

    def searchItems(self, criteria):
        self.fetchAll()

        items = self.books + self.magazines
        results = []

        for item in items:
            for key in criteria:
                match key:
                    case "title":
                        if criteria[key] == "":
                            results.append(item)
                        else:
                            title = item.getData()[key].lower()
                            comparator = criteria[key].lower()
        
                            results.append(item) if (comparator in title) else None

                    case "author":
                        if criteria[key] == "":
                            None
                        else:
                            for index, result in enumerate(results):
                                author = result.getData()[key].lower()
                                comparator = criteria[key].lower()

                                results.pop(index) if (comparator not in author) else None
                    
                    case "price":
                        if criteria[key] == "":
                            None
                        else:
                            for index, result in enumerate(results):
                                price = float(result.getData()[key])
                                comparator = float(criteria[key])

                                operator = criteria["operator"]

                                match operator:
                                    case "not":
                                        results.pop(index) if (comparator != price) else None
                                    case "less":
                                        results.pop(index) if (comparator <= price) else None
                                    case "greater":
                                        results.pop(index) if (comparator >= price) else None

        return results
