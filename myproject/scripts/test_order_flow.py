import os
import django
import json
from decimal import Decimal
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
# Ensure project root is on sys.path (script may run with cwd inside the project folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
django.setup()

from django.contrib.auth import get_user_model
from myapp.models import Store, Book, Order
from django.test import Client

User = get_user_model()


def get_or_create_user(username, password, email):
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    if created:
        user.set_password(password)
        user.save()
    return user


customer = get_or_create_user('test_customer', 'testpass', 'cust@example.com')
owner = get_or_create_user('store_owner', 'ownerpass', 'owner@example.com')

store, _ = Store.objects.get_or_create(
    store_name='Test Store',
    defaults={
        'owner_full_name': owner.username,
        'email': owner.email,
        'phone': '1234567890',
        'store_type': 'books',
        'city': 'TestCity',
        'address': '123 Test St',
        'store_description': 'Auto-created test store',
        'offers_sale': True,
        'offers_rental': True,
        'offers_delivery': True,
    }
)

book, _ = Book.objects.get_or_create(
    title='Test Book',
    store=store,
    defaults={
        'author': 'Author X',
        'genre': 'fiction',
        'publication_year': 2020,
        'total_copies': 5,
        'available_copies': 5,
        'available_sales': 5,
        'rental_price': Decimal('1.00'),
        'sale_price': Decimal('5.00'),
    }
)

print('Customer:', customer.username, 'Owner:', owner.username)
print('Store:', store.store_name, 'Book id:', book.id)

# Customer places order
c = Client()
logged = c.login(username='test_customer', password='testpass')
print('Customer login:', logged)

session = c.session
session['cart'] = {'rental': [book.id], 'purchase': []}
session.save()

payload = {
    'delivery_option': 'pickup',
    'delivery_fee': '0',
    'rental_days': 7,
    'notes': 'Test order via script'
}

resp = c.post('/create-order/', json.dumps(payload), content_type='application/json', HTTP_HOST='localhost')
print('create-order response:', resp.status_code, resp.content)

orders = Order.objects.filter(customer=customer).order_by('-created_at')
print('Orders for customer:', orders.count())
if orders.exists():
    order = orders.first()
    print('Created order id:', order.id, 'number:', order.order_number, 'status:', order.status)

    # Store owner approves the order
    oc = Client()
    ok = oc.login(username='store_owner', password='ownerpass')
    print('Owner login:', ok)
    proc = oc.post(f'/store/order/process/{order.id}/', {'status': 'preparing'}, HTTP_HOST='localhost')
    print('process POST status:', proc.status_code)
    order.refresh_from_db()
    print('Order status after processing:', order.status)
else:
    print('No order created')
