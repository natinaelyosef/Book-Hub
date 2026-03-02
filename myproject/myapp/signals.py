from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


DEFAULT_SUPERADMIN_USERNAME = "superadmin"
DEFAULT_SUPERADMIN_EMAIL = "superadmin@gmail.com"
DEFAULT_SUPERADMIN_PASSWORD = "password12345678"


@receiver(post_migrate)
def ensure_default_super_admin(sender, **kwargs):
    if sender.name != "myapp":
        return

    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        username=DEFAULT_SUPERADMIN_USERNAME,
        defaults={
            "email": DEFAULT_SUPERADMIN_EMAIL,
            "is_staff": True,
            "is_superuser": True,
        },
    )

    has_changes = False

    if user.email != DEFAULT_SUPERADMIN_EMAIL:
        user.email = DEFAULT_SUPERADMIN_EMAIL
        has_changes = True

    if not user.is_staff:
        user.is_staff = True
        has_changes = True

    if not user.is_superuser:
        user.is_superuser = True
        has_changes = True

    # Set the default password only for newly created accounts.
    if created:
        user.set_password(DEFAULT_SUPERADMIN_PASSWORD)
        has_changes = True

    if has_changes:
        user.save()
