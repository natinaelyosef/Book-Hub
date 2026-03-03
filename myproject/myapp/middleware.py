from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

from .models import AccountRestriction


class AccountRestrictionMiddleware:
    """Prevents suspended/deleted accounts from using authenticated areas."""

    EXEMPT_PREFIXES = (
        '/login/',
        '/accounts/login/',
        '/logout/',
        '/register/',
        '/admin/login/',
        '/admin/normal/login/',
        '/assets/',
        '/media/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated or request.user.is_superuser:
            return self.get_response(request)

        if any(request.path.startswith(prefix) for prefix in self.EXEMPT_PREFIXES):
            return self.get_response(request)

        restriction = AccountRestriction.objects.filter(user=request.user).first()
        if not restriction:
            return self.get_response(request)

        if restriction.is_deleted:
            reason = restriction.deleted_reason or 'No reason was provided.'
            auth_logout(request)
            messages.error(request, f'Your account has been deleted. Reason: {reason}')
            return redirect('login')

        if restriction.is_currently_suspended():
            auth_logout(request)
            messages.error(request, restriction.status_message())
            return redirect('login')

        return self.get_response(request)


class AdminNoCacheMiddleware:
    """Disables browser caching for admin pages to prevent back-button access after logout."""

    ADMIN_PREFIXES = (
        '/dashboard_super/',
        '/dashboard_admin/',
        '/super_admin/',
        '/register_admin/',
        '/admin/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if any(request.path.startswith(prefix) for prefix in self.ADMIN_PREFIXES):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response
