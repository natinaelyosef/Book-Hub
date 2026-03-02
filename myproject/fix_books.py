# fix_books.py
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Book

def fix_book_availability():
    books = Book.objects.all()
    
    for book in books:
        print(f"Checking book: {book.title}")
        before_ac = getattr(book, 'available_copies', None)
        before_as = getattr(book, 'available_sales', None)
        total = getattr(book, 'total_copies', 0) or 0
        print(f"  Before - Available Copies: {before_ac}, Available Sales: {before_as}, Total: {total}")

        changed = False
        # If book has total copies but no available copies/sales, set them
        if total > 0:
            if (before_ac in (None, 0)) and (before_as in (None, 0)):
                # Distribute copies between rental and sales
                ac = total // 2
                asales = total - ac
                book.available_copies = ac
                book.available_sales = asales
                changed = True

        # Ensure non-negative integers
        if getattr(book, 'available_copies', 0) is None or book.available_copies < 0:
            book.available_copies = 0
            changed = True
        if getattr(book, 'available_sales', 0) is None or book.available_sales < 0:
            book.available_sales = 0
            changed = True

        if changed:
            book.save()
            print(f"  After - Available Copies: {book.available_copies}, Available Sales: {book.available_sales}")
    
    print("Book availability fixed!")

if __name__ == "__main__":
    fix_book_availability()