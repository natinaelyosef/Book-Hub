from django.db import models
from django.conf import settings

# Create your models here.
class Features(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=255)
    is_truee = models.BooleanField(default=False)


class Store(models.Model):
    store_name = models.CharField(max_length=100)
    owner_full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    store_type = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    store_description = models.TextField()
    offers_rental = models.BooleanField(default=False)
    offers_sale = models.BooleanField(default=False)
    offers_delivery = models.BooleanField(default=False)
    delivery_radius = models.CharField(max_length=50, null=True, blank=True)
    delivery_fee = models.CharField(max_length=50, null=True, blank=True)
    delivery_bike = models.BooleanField(default=False)
    delivery_car = models.BooleanField(default=False)
    delivery_pickup = models.BooleanField(default=False)
    open_monday = models.BooleanField(default=False)
    open_time_monday = models.TimeField(null=True, blank=True)
    close_time_monday = models.TimeField(null=True, blank=True)

    open_tuesday = models.BooleanField(default=False)
    open_time_tuesday = models.TimeField(null=True, blank=True)
    close_time_tuesday = models.TimeField(null=True, blank=True)

    open_wednesday = models.BooleanField(default=False)
    open_time_wednesday = models.TimeField(null=True, blank=True)
    close_time_wednesday = models.TimeField(null=True, blank=True)

    open_thursday = models.BooleanField(default=False)
    open_time_thursday = models.TimeField(null=True, blank=True)
    close_time_thursday = models.TimeField(null=True, blank=True)

    open_friday = models.BooleanField(default=False)
    open_time_friday = models.TimeField(null=True, blank=True)
    close_time_friday = models.TimeField(null=True, blank=True)

    open_saturday = models.BooleanField(default=False)
    open_time_saturday = models.TimeField(null=True, blank=True)
    close_time_saturday = models.TimeField(null=True, blank=True)

    open_sunday = models.BooleanField(default=False)
    open_time_sunday = models.TimeField(null=True, blank=True)
    close_time_sunday = models.TimeField(null=True, blank=True)

    # Additional fields added to support registration form data
    rental_period = models.CharField(max_length=50, null=True, blank=True)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_books = models.IntegerField(null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    payment_methods = models.CharField(max_length=200, null=True, blank=True)
    agree_terms = models.BooleanField(default=False)

    in_stock = models.BooleanField(default=True)














# models.py
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, default='fiction')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    total_copies = models.IntegerField(default=0)
    available_copies = models.IntegerField(default=0)
    available_sales = models.IntegerField(default=0)
    rental_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"




class add_book_registration(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    genre = models.CharField(max_length=50)
    publication_year = models.IntegerField(null=True, blank=True)
    total_copies = models.IntegerField(null=True, blank=True, default=0)
    available_copies = models.IntegerField(null=True, blank=True, default=0)
    available_sales = models.IntegerField(null=True, blank=True, default=0)

    rental_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    # cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return self.title

# Provide a backwards-compatible alias so views referencing `Book`
# (existing code) continue to work without renaming the model class.











# Add these models to your existing models.py

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('contacted', 'Contacted'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup/Delivery'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Declined'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('pending', 'Pending'),
    ]
    
    ORDER_TYPE_CHOICES = [
        ('rent', 'Rental'),
        ('buy', 'Purchase'),
        ('mixed', 'Mixed'),
    ]
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    order_type = models.CharField(max_length=10, choices=ORDER_TYPE_CHOICES)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, default='pending')
    delivery_option = models.CharField(max_length=20)  # pickup, delivery
    delivery_address = models.TextField(blank=True, null=True)
    preferred_time = models.CharField(max_length=50, blank=True, null=True)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    rental_days = models.IntegerField(null=True, blank=True)  # for rentals only
    notes = models.TextField(blank=True, null=True)
    store_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.order_number} - {self.customer.username}"

    def _generate_order_number(self):
        next_num = 1001
        latest = (
            Order.objects.exclude(order_number__isnull=True)
            .exclude(order_number='')
            .filter(order_number__startswith='ORD-')
            .order_by('-id')
            .first()
        )
        if latest:
            try:
                latest_num = int(latest.order_number.split('-')[1])
                next_num = max(next_num, latest_num + 1)
            except (IndexError, ValueError):
                pass

        candidate = f"ORD-{next_num:04d}"
        while Order.objects.filter(order_number=candidate).exists():
            next_num += 1
            candidate = f"ORD-{next_num:04d}"
        return candidate

    def save(self, *args, **kwargs):
        if not (self.order_number or '').strip():
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_days = models.IntegerField(null=True, blank=True)
    item_type = models.CharField(max_length=10)  # rent or buy
    
    def __str__(self):
        return f"{self.book.title} - {self.order.order_number}"


class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('on_the_way', 'On the Way'),
        ('delivered', 'Delivered'),
        ('failed', 'Delivery Failed'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=100, blank=True, null=True)
    driver_phone = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending')
    estimated_arrival = models.DateTimeField(null=True, blank=True)
    current_location = models.CharField(max_length=200, blank=True, null=True)
    delivery_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Delivery for {self.order.order_number}"


class CustomerReview(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.username} - {self.store.store_name}"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

