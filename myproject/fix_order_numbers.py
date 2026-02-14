# fix_order_numbers.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Order

def fix_order_numbers():
    orders = Order.objects.filter(order_number__isnull=True) | Order.objects.filter(order_number='')
    count = 0
    
    for order in orders:
        # Generate order number like ORD-1001
        last_order = Order.objects.exclude(order_number__isnull=True).exclude(order_number='').order_by('id').last()
        if last_order and last_order.order_number:
            try:
                last_num = int(last_order.order_number.split('-')[1])
                order.order_number = f"ORD-{last_num + 1:04d}"
            except:
                order.order_number = f"ORD-{1000 + order.id:04d}"
        else:
            order.order_number = f"ORD-{1000 + order.id:04d}"
        
        order.save()
        count += 1
    
    print(f"Fixed {count} orders with missing order numbers")

if __name__ == '__main__':
    fix_order_numbers()