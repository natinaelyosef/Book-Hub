from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Features(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=255)
    is_truee = models.BooleanField(default=False)


class Store(models.Model):
    store_name = models.CharField(max_length=100)
    owner_full_name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_stores'
    )
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


# Book model with image field
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
    # Add this line for book cover image
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
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
    # Add this line for book cover image
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def __str__(self):
        return self.title


# Order models
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














# Add to your existing models.py

class Conversation(models.Model):
    """Represents a conversation between a customer and a store"""
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer_conversations')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_conversations')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('customer', 'store', 'book')  # One conversation per customer-store-book
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.customer.username} - {self.store.store_name} - {self.book.title if self.book else 'General'}"
    
    def last_message(self):
        return self.messages.order_by('-timestamp').first()
    
    def unread_count(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    """Individual messages within a conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
    
    from django.utils import timezone
    from datetime import timedelta
    def formatted_time(self):
        now = timezone.now()
        if self.timestamp.date() == now.date():
            return self.timestamp.strftime('%I:%M %p')
        elif self.timestamp.date() == (now.date() - timedelta(days=1)):
            return 'Yesterday'
        else:
            return self.timestamp.strftime('%b %d, %Y')


class AdminAccount(models.Model):
    """Normal admin accounts managed by the super admin."""
    STATUS_ACTIVE = "active"
    STATUS_SUSPENDED = "suspended"
    STATUS_DELETED = "deleted"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_SUSPENDED, "Suspended"),
        (STATUS_DELETED, "Deleted"),
    ]

    name = models.CharField(max_length=150)
    admin_type = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='admin_profile_images/', blank=True, null=True)
    ref_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    suspension_reason = models.TextField(blank=True, null=True)
    suspension_until = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='created_admin_accounts',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def is_currently_suspended(self):
        if self.status != self.STATUS_SUSPENDED:
            return False
        if self.suspension_until and self.suspension_until <= timezone.now():
            self.status = self.STATUS_ACTIVE
            self.suspension_until = None
            self.suspension_reason = ""
            self.save(update_fields=['status', 'suspension_until', 'suspension_reason'])
            return False
        return True

    def __str__(self):
        return f"{self.name} ({self.ref_number})"


class AccountRestriction(models.Model):
    """Tracks suspension/deletion state for customer and store-owner accounts."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_restriction')
    is_suspended = models.BooleanField(default=False)
    suspended_reason = models.TextField(blank=True, null=True)
    suspended_until = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_reason = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def is_currently_suspended(self):
        if not self.is_suspended:
            return False
        if self.suspended_until and self.suspended_until <= timezone.now():
            self.is_suspended = False
            self.suspended_reason = ""
            self.suspended_until = None
            self.save(update_fields=['is_suspended', 'suspended_reason', 'suspended_until', 'updated_at'])
            if not self.is_deleted and not self.user.is_active:
                self.user.is_active = True
                self.user.save(update_fields=['is_active'])
            return False
        return True

    def status_message(self):
        if self.is_deleted:
            reason = self.deleted_reason or "No reason was provided."
            return f"Your account has been deleted. Reason: {reason}"
        if self.is_currently_suspended():
            reason = self.suspended_reason or "No reason was provided."
            if self.suspended_until:
                date_text = timezone.localtime(self.suspended_until).strftime('%Y-%m-%d %H:%M')
                return f"Your account is suspended until {date_text}. Reason: {reason}"
            return f"Your account is suspended. Reason: {reason}"
        return ""

    def __str__(self):
        return f"Restriction<{self.user.username}>"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    avatar = models.ImageField(upload_to='profile_avatars/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Profile<{self.user.username}>"


class IssueReport(models.Model):
    ROLE_CUSTOMER = "customer"
    ROLE_STORE_OWNER = "store_owner"
    ROLE_CHOICES = [
        (ROLE_CUSTOMER, "Customer"),
        (ROLE_STORE_OWNER, "Store Owner"),
    ]

    STATUS_PENDING = "pending"
    STATUS_UNDER_REVIEW = "under_review"
    STATUS_RESOLVED = "resolved"
    STATUS_REJECTED = "rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_UNDER_REVIEW, "Under Review"),
        (STATUS_RESOLVED, "Resolved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    CATEGORY_FRAUD = "fraud"
    CATEGORY_POOR_SERVICE = "poor_service"
    CATEGORY_INAPPROPRIATE = "inappropriate_behavior"
    CATEGORY_POLICY_VIOLATION = "policy_violation"
    CATEGORY_ABUSIVE = "abusive_behavior"
    CATEGORY_FAKE_ORDER = "fake_order"
    CATEGORY_PAYMENT_ISSUE = "payment_issue"
    CATEGORY_MISUSE = "misuse_platform"
    CATEGORY_OTHER = "other"
    CATEGORY_CHOICES = [
        (CATEGORY_FRAUD, "Fraud"),
        (CATEGORY_POOR_SERVICE, "Poor Service"),
        (CATEGORY_INAPPROPRIATE, "Inappropriate Behavior"),
        (CATEGORY_POLICY_VIOLATION, "Policy Violation"),
        (CATEGORY_ABUSIVE, "Abusive Behavior"),
        (CATEGORY_FAKE_ORDER, "Fake Order"),
        (CATEGORY_PAYMENT_ISSUE, "Payment Issue"),
        (CATEGORY_MISUSE, "Misuse of Platform"),
        (CATEGORY_OTHER, "Other"),
    ]

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submitted_issue_reports')
    reporter_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_issue_reports')
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    description = models.TextField()
    attachment = models.FileField(upload_to='issue_attachments/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    assigned_sub_admin = models.ForeignKey(
        AdminAccount,
        on_delete=models.SET_NULL,
        related_name='assigned_issue_reports',
        null=True,
        blank=True,
    )
    reviewed_by = models.ForeignKey(
        AdminAccount,
        on_delete=models.SET_NULL,
        related_name='reviewed_issue_reports',
        null=True,
        blank=True,
    )
    reviewed_by_super_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='super_admin_reviewed_issue_reports',
        null=True,
        blank=True,
    )
    resolution_note = models.TextField(blank=True, null=True)
    escalated_to_admin = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Report #{self.id} - {self.reporter.username} -> {self.reported_user.username}"


class SupportConversation(models.Model):
    TARGET_SUB_ADMIN = "sub_admin"
    TARGET_ADMIN = "admin"
    TARGET_CHOICES = [
        (TARGET_SUB_ADMIN, "Sub-Admin"),
        (TARGET_ADMIN, "Admin"),
    ]

    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_conversations')
    user_role = models.CharField(max_length=20, choices=IssueReport.ROLE_CHOICES)
    issue_report = models.ForeignKey(IssueReport, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_conversations')
    subject = models.CharField(max_length=255, blank=True)
    assigned_sub_admin = models.ForeignKey(
        AdminAccount,
        on_delete=models.SET_NULL,
        related_name='support_conversations',
        null=True,
        blank=True,
    )
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, default=TARGET_SUB_ADMIN)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"SupportChat #{self.id} - {self.user.username} ({self.target})"


class SupportMessage(models.Model):
    ROLE_SUB_ADMIN = "sub_admin"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = IssueReport.ROLE_CHOICES + [
        (ROLE_SUB_ADMIN, "Sub-Admin"),
        (ROLE_ADMIN, "Admin"),
    ]

    conversation = models.ForeignKey(SupportConversation, on_delete=models.CASCADE, related_name='messages')
    sender_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_support_messages',
    )
    sender_sub_admin = models.ForeignKey(
        AdminAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_support_messages',
    )
    sender_role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='support_attachments/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"SupportMessage #{self.id} ({self.sender_role})"


class ModerationActivityLog(models.Model):
    ACTOR_CUSTOMER = "customer"
    ACTOR_STORE_OWNER = "store_owner"
    ACTOR_SUB_ADMIN = "sub_admin"
    ACTOR_ADMIN = "admin"
    ACTOR_SYSTEM = "system"
    ACTOR_CHOICES = [
        (ACTOR_CUSTOMER, "Customer"),
        (ACTOR_STORE_OWNER, "Store Owner"),
        (ACTOR_SUB_ADMIN, "Sub-Admin"),
        (ACTOR_ADMIN, "Admin"),
        (ACTOR_SYSTEM, "System"),
    ]

    action = models.CharField(max_length=80)
    actor_role = models.CharField(max_length=20, choices=ACTOR_CHOICES)
    actor_name = models.CharField(max_length=150)
    target_type = models.CharField(max_length=40)
    target_identifier = models.CharField(max_length=255)
    reason = models.TextField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.actor_role} - {self.action} - {self.target_type}"
