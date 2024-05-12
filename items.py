from abc import ABC, abstractmethod
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