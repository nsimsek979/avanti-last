from .models import ContactInfo

def contact_info(request):
    """Make contact info available in all templates"""
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    return {
        'contact_info': contact_info
    }
