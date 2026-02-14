import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Book, Store

def assign_stores_to_books():
    # Get the first store (or create one if none exists)
    stores = Store.objects.all()
    
    if not stores.exists():
        print("❌ No stores found in database. Please create a store first.")
        return
    
    # Get all books without a store
    books_without_store = Book.objects.filter(store__isnull=True)
    count = books_without_store.count()
    
    if count == 0:
        print("✅ All books already have stores assigned!")
        return
    
    print(f"📚 Found {count} books without a store")
    
    # Assign the first store to all books without a store
    store = stores.first()
    books_without_store.update(store=store)
    
    print(f"✅ Assigned store '{store.store_name}' to {count} books")

def check_books_status():
    """Check the status of all books"""
    total_books = Book.objects.count()
    books_with_store = Book.objects.filter(store__isnull=False).count()
    books_without_store = Book.objects.filter(store__isnull=True).count()
    
    print("\n=== BOOKS STATUS ===")
    print(f"Total books: {total_books}")
    print(f"Books with store: {books_with_store}")
    print(f"Books without store: {books_without_store}")
    
    # Show sample of books without store
    if books_without_store > 0:
        print("\n📋 Sample of books without store:")
        for book in Book.objects.filter(store__isnull=True)[:5]:
            print(f"  - {book.title} by {book.author} (ID: {book.id})")
    
    # Show sample of books with store
    if books_with_store > 0:
        print("\n📋 Sample of books with store:")
        for book in Book.objects.filter(store__isnull=False)[:5]:
            print(f"  - {book.title} by {book.author} - Store: {book.store.store_name}")

if __name__ == "__main__":
    print("🔧 Fixing book store assignments...")
    check_books_status()
    assign_stores_to_books()
    check_books_status()