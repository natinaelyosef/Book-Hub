import os
import django
import sys
from pathlib import Path
# Ensure project parent directory is on sys.path so `import myproject` works
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myproject.settings')
django.setup()
from myapp.models import Book

titles = ['mat', 'naty', 'naty3']
books = Book.objects.filter(title__in=titles)
cnt = 0
for b in books:
    b.store = None
    b.save()
    cnt += 1
print(f'unset store for {cnt} books')
