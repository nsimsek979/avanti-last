from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory, ServiceType

def service_list(request):
    context = {
        'service_types': ServiceType.objects.filter(is_active=True).prefetch_related('categories__services'),
    }
    return render(request, 'services/service_list.html', context)

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    context = {
        'service': service,
        'related_services': Service.objects.filter(
            category=service.category, 
            is_active=True
        ).exclude(id=service.id)[:3],
    }
    return render(request, 'services/service_detail.html', context)
