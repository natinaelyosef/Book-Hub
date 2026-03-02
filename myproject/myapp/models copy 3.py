from django.db import models

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

