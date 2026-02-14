from django.core.management.base import BaseCommand
from myapp.models import Book, Store
from django.db.models import Q

class Command(BaseCommand):
    help = 'Assign stores to books that dont have one'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to fix book store assignments...'))
        
        # Check if there are any stores
        stores = Store.objects.all()
        
        if not stores.exists():
            self.stdout.write(self.style.ERROR('No stores found in database!'))
            self.stdout.write(self.style.WARNING('Please create a store first.'))
            return
        
        # Get the first store (or you can modify this to assign based on some logic)
        default_store = stores.first()
        
        # Find books without store
        books_without_store = Book.objects.filter(store__isnull=True)
        count = books_without_store.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('All books already have stores assigned!'))
        else:
            # Assign store to books
            books_without_store.update(store=default_store)
            self.stdout.write(
                self.style.SUCCESS(f'✅ Assigned store "{default_store.store_name}" to {count} books')
            )
        
        # Show summary
        total_books = Book.objects.count()
        books_with_store = Book.objects.filter(store__isnull=False).count()
        books_without_store = Book.objects.filter(store__isnull=True).count()
        
        self.stdout.write("\n=== BOOKS STATUS ===")
        self.stdout.write(f"Total books: {total_books}")
        self.stdout.write(f"Books with store: {books_with_store}")
        self.stdout.write(f"Books without store: {books_without_store}")
        
        # Show sample
        if books_with_store > 0:
            self.stdout.write("\n📋 Sample books with store:")
            for book in Book.objects.filter(store__isnull=False)[:3]:
                self.stdout.write(f"  - {book.title} - Store: {book.store.store_name}")