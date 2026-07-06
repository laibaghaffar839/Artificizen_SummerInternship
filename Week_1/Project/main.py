import json
import os



# Custom Exceptions
class BookNotFoundError(Exception):
    pass


class NoCopiesAvailableError(Exception):
    pass


class AlreadyBorrowedError(Exception):
    pass


class BookNotBorrowedError(Exception):
    pass



# Book Class

class Book:
    def __init__(self, title, author, isbn, copies_available):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies_available = copies_available

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "copies_available": self.copies_available,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["author"],
            data["isbn"],
            data["copies_available"],
        )

    def __str__(self):
        return (
            f"{self.title} by {self.author} "
            f"(ISBN: {self.isbn}) - Copies: {self.copies_available}"
        )



# Member Class

class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def to_dict(self):
        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": self.borrowed_books,
        }

    @classmethod
    def from_dict(cls, data):
        member = cls(data["name"], data["member_id"])
        member.borrowed_books = data["borrowed_books"]
        return member

    def __str__(self):
        return f"{self.name} ({self.member_id})"



# Library Class

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = {}
        self.members = {}
        self.load_data()

    # Books 
    def add_book(self, book):
        if book.isbn in self.books:
            self.books[book.isbn].copies_available += book.copies_available
        else:
            self.books[book.isbn] = book

        self.save_data()

    def search_book(self, keyword):
        found = []

        for book in self.books.values():
            if (
                keyword.lower() in book.title.lower()
                or keyword.lower() in book.author.lower()
                or keyword == book.isbn
            ):
                found.append(book)

        if not found:
            raise BookNotFoundError("Book not found.")

        return found

    # Members 
    def add_member(self, member):
        self.members[member.member_id] = member
        self.save_data()

    # Issue 
    def issue_book(self, member_id, isbn):

        if isbn not in self.books:
            raise BookNotFoundError("Book not found.")

        book = self.books[isbn]

        if book.copies_available == 0:
            raise NoCopiesAvailableError("No copies available.")

        member = self.members.get(member_id)

        if member is None:
            raise Exception("Member not found.")

        if isbn in member.borrowed_books:
            raise AlreadyBorrowedError("Member already borrowed this book.")

        member.borrowed_books.append(isbn)
        book.copies_available -= 1

        self.save_data()

    # Return 
    def return_book(self, member_id, isbn):

        member = self.members.get(member_id)

        if member is None:
            raise Exception("Member not found.")

        if isbn not in member.borrowed_books:
            raise BookNotBorrowedError("This member never borrowed this book.")

        member.borrowed_books.remove(isbn)
        self.books[isbn].copies_available += 1

        self.save_data()

    # JSON
    def save_data(self):

        data = {
            "books": {
                isbn: book.to_dict()
                for isbn, book in self.books.items()
            },
            "members": {
                mid: member.to_dict()
                for mid, member in self.members.items()
            },
        }

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):

        if not os.path.exists(self.filename):
            return

        with open(self.filename, "r") as file:
            data = json.load(file)

        self.books = {
            isbn: Book.from_dict(book)
            for isbn, book in data.get("books", {}).items()
        }

        self.members = {
            mid: Member.from_dict(member)
            for mid, member in data.get("members", {}).items()
        }



# Testing

library = Library()

# Add books
library.add_book(Book("Python", "Ahmed", "ISBN001", 3))
library.add_book(Book("Java", "Ali", "ISBN002", 2))

# Add members
library.add_member(Member("Hassan", "M001"))
library.add_member(Member("Areeba", "M002"))

# Search
try:
    books = library.search_book("Python")
    for b in books:
        print(b)
except BookNotFoundError as e:
    print(e)

# Issue
try:
    library.issue_book("M001", "ISBN001")
    print("Book Issued Successfully")
except Exception as e:
    print(e)

# Return
try:
    library.return_book("M001", "ISBN001")
    print("Book Returned Successfully")
except Exception as e:
    print(e)