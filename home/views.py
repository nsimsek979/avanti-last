from django.shortcuts import render
from .models import HeroSection, WhyChooseUs
from services.models import ServiceType
from about.models import Story, OurApproach

def index(request):
    context = {
        'hero_sections': HeroSection.objects.filter(is_active=True),
        'why_choose_us': WhyChooseUs.objects.filter(is_active=True),
        'service_types': ServiceType.objects.filter(is_active=True).prefetch_related('categories'),
        'story': Story.objects.filter(is_active=True).first(),
        'approaches': OurApproach.objects.filter(is_active=True),
    }
    return render(request, 'home/index.html', context)
