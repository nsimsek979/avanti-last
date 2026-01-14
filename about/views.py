from django.shortcuts import render
from .models import Story, OurApproach
from home.models import WhyChooseUs

def about(request):
    context = {
        'stories': Story.objects.filter(is_active=True),
        'approaches': OurApproach.objects.filter(is_active=True),
        'why_choose_items': WhyChooseUs.objects.filter(is_active=True),
    }
    return render(request, 'about/about.html', context)
