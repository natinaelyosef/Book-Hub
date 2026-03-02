import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myproject.settings')
import django
django.setup()
from myapp.models import Book
q='naty'
qs=Book.objects.filter(title__icontains=q)
print('count:', qs.count())
print('titles:', list(qs.values_list('title', flat=True)[:50]))
