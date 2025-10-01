# middleware.py
import os
import geoip2.database
from django.conf import settings
from .models import Visitor

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Initialize the reader once when middleware loads
        self.reader = geoip2.database.Reader(os.path.join(settings.GEOIP_PATH, 'GeoLite2-City.mmdb'))
        
    def __call__(self, request):
        if not request.path.startswith('/admin/'):
            try:
                ip = self.get_client_ip(request)
                if ip:
                    try:
                        response = self.reader.city(ip)
                        country = response.country.name
                        city = response.city.name
                    except:
                        country = city = None
                    
                    Visitor.objects.create(
                        ip_address=ip,
                        country=country,
                        city=city,
                        # ... other fields
                    )
            except Exception as e:
                print(f"Tracking error: {e}")
                
        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')