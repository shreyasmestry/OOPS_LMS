from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional


class Book:
    """Represents a book in the library system."""

    def __init__(self, isbn: str, title: str, author: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self._is_available = True  # Encapsulation: internal state

    @property
    def is_available(self) -> bool:
        return self._is_available

    def borrow_book(self) -> bool:
        if self._is_available:
            self._is_available = False
            return True
        return False

    def return_book(self):
        self._is_available = True

    def __str__(self) -> str:
        status = "Available" if self._is_available else "Borrowed"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - [{status}]"


class User(ABC):
    """Abstract Base Class representing a generic User (Abstraction)."""

    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    @abstractmethod
    def get_role(self) -> str:
        """Polymorphic method to get user role."""
        pass


class Librarian(User):
    """Represents a Librarian who manages the library (Inheritance)."""

    def get_role(self) -> str:
        return "Librarian"

    def add_book_to_library(self, library: "Library", book: Book):
        library.add_book(book)
        print(f"[Librarian {self.name}] Added book: {book.title}")

    def remove_book_from_library(self, library: "Library", isbn: str):
        library.remove_book(isbn)


class Member(User):
    """Represents a Library Member who borrows books (Inheritance)."""

    def __init__(self, user_id: str, name: str, member_type: str = "Regular"):
        super().__init__(user_id, name)
        self.member_type = member_type
        self.borrowed_books = {}  # Stores {Book: due_date}

    def get_role(self) -> str:
        return f"{self.member_type} Member"

    # Polymorphism: Max books allowed depends on membership type
    @property
    def max_borrow_limit(self) -> int:
        return 5 if self.member_type == "Premium" else 2

    def borrow_item(self, book: Book) -> bool:
        if len(self.borrowed_books) >= self.max_borrow_limit:
            print(f"❌ {self.name} has reached their limit of {self.max_borrow_limit} books.")
            return False

        if book.borrow_book():
            # Set due date to 14 days from now
            due_date = datetime.now() + timedelta(days=14)
            self.borrowed_books[book] = due_date
            print(f"✅ {self.name} successfully borrowed '{book.title}'. Due: {due_date.strftime('%Y-%m-%d')}")
            return True
        else:
            print(f"❌ '{book.title}' is currently unavailable.")
            return False

    def return_item(self, book: Book):
        if book in self.borrowed_books:
            due_date = self.borrowed_books.pop(book)
            book.return_book()
            
            # Simple fine calculation demo (simulating a late return)
            if datetime.now() > due_date:
                print(f"⚠️ Book returned late! Fine incurred.")
            else:
                print(f"✅ {self.name} returned '{book.title}' on time.")
        else:
            print(f"❌ {self.name} does not have this book checked out.")


class Library:
    """Manages the collection of books and users."""

    def __init__(self):
        self._books: List[Book] = []  # Encapsulation

    def add_book(self, book: Book):
        self._books.append(book)

    def remove_book(self, isbn: str):
        book = self.search_by_isbn(isbn)
        if book:
            self._books.remove(book)
            print(f"Removed book: {book.title}")
        else:
            print("Book not found.")

    def search_by_title(self, title: str) -> List[Book]:
        return [b for b in self._books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        for book in self._books:
            if book.isbn == isbn:
                return book
        return None

    def display_catalog(self):
        print("\n--- Library Catalog ---")
        if not self._books:
            print("The library is empty.")
        for book in self._books:
            print(book)
        print("-----------------------\n")


# ==========================================
# DEMONSTRATION WORKFLOW
# ==========================================
if __name__ == "__main__":
    # 1. Initialize Library
    my_library = Library()

    # 2. Create Users (Librarian and Members)
    librarian = Librarian(user_id="L001", name="Sarah")
    regular_member = Member(user_id="M001", name="Alice", member_type="Regular")
    premium_member = Member(user_id="M002", name="Bob", member_type="Premium")

    # 3. Librarian adds books to the library
    book1 = Book("978-0141187761", "1984", "George Orwell")
    book2 = Book("978-0345339683", "The Hobbit", "J.R.R. Tolkien")
    book3 = Book("978-0618640157", "The Fellowship of the Ring", "J.R.R. Tolkien")

    print("--- Librarian Actions ---")
    librarian.add_book_to_library(my_library, book1)
    librarian.add_book_to_library(my_library, book2)
    librarian.add_book_to_library(my_library, book3)

    # Display starting catalog
    my_library.display_catalog()

    # 4. Members searching and borrowing books
    print("--- Member Actions (Borrowing) ---")
    # Regular Member borrows books up to limit (Limit = 2)
    regular_member.borrow_item(book1)
    regular_member.borrow_item(book2)
    regular_member.borrow_item(book3)  # Should fail due to limit

    # Premium member tries to borrow the already borrowed book1
    print("\n--- Premium Member Actions ---")
    premium_member.borrow_item(book1)  # Should fail (unavailable)
    premium_member.borrow_item(book3)  # Should succeed

    # Check status after borrowing
    my_library.display_catalog()

    # 5. Returning books
    print("--- Member Actions (Returning) ---")
    regular_member.return_item(book1)
    
    # Premium member can now borrow book1 since it's returned
    premium_member.borrow_item(book1)

    # Final Catalog State
    my_library.display_catalog()