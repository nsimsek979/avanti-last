from django.utils import timezone
from .models import Visitor, PageView
import threading


def get_client_ip(request):
    """Get the real IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AnalyticsMiddleware:
    """
    Middleware to track visitors and page views.
    Only counts unique visitors per session (not per page view).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip tracking for admin, static, and media URLs
        if not any(request.path.startswith(path) for path in ['/admin/', '/static/', '/media/', '/i18n/']):
            self.track_visitor(request)
        
        response = self.get_response(request)
        return response
    
    def track_visitor(self, request):
        """Track visitor with session-based uniqueness"""
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()
        
        session_key = request.session.session_key
        ip_address = get_client_ip(request)
        
        # Check if visitor already exists for this session
        visitor, created = Visitor.objects.get_or_create(
            session_key=session_key,
            defaults={
                'ip_address': ip_address,
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500],
            }
        )
        
        if not created:
            # Update existing visitor
            visitor.page_views += 1
            visitor.last_visit = timezone.now()
            visitor.save(update_fields=['page_views', 'last_visit'])
        else:
            # New visitor - get location data in background
            if ip_address and not ip_address.startswith('127.') and ip_address != '::1':
                thread = threading.Thread(target=visitor.get_location_from_ip)
                thread.daemon = True
                thread.start()
        
        # Track page view
        PageView.objects.create(
            visitor=visitor,
            url=request.path,
            title=request.path.strip('/').replace('/', ' > ').title() or 'Home',
            referrer=request.META.get('HTTP_REFERER', '')[:500]
        )
