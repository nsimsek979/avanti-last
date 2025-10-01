from django.shortcuts import render
from django.utils.translation import get_language
from .models import (
    Index, IndexContent, OurApproach, OurApproachContent, ChooseUs, ChooseUsContent,  
    Clients, SourcingSolutions, SourcingSolutionsContent, 
    ConsultancyServices, ConsultancyServicesContent, Visitor, OurStory, OurStoryContent,
    Service, ServiceContent, ProductCategory, ProductCategoryContent, Products, ProductsContent, 
    Address, AddressContent
)
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.utils import timezone
from datetime import timedelta
from django.db import models


def get_content_for_language(model_class, content_class, language_code):
    """Helper function to get content for current language with fallback to English"""
    try:
        # Get active items with content in the current language
        items = model_class.objects.filter(is_active=True).prefetch_related(
            f'{content_class._meta.model_name.lower().replace(model_class._meta.model_name.lower(), "")}_content__language'
        )
        
        result = []
        for item in items:
            # Get content for current language
            content = item._meta.get_field(f'{content_class._meta.model_name.lower().replace(model_class._meta.model_name.lower(), "")}_content').related_model.objects.filter(
                **{item._meta.model_name.lower(): item, 'language__code': language_code}
            ).first()
            
            # Fallback to English if current language not found
            if not content:
                content = item._meta.get_field(f'{content_class._meta.model_name.lower().replace(model_class._meta.model_name.lower(), "")}_content').related_model.objects.filter(
                    **{item._meta.model_name.lower(): item, 'language__code': 'en'}
                ).first()
            
            if content:
                # Combine item and content
                item.content = content
                result.append(item)
        
        return result
    except Exception as e:
        print(f"Error getting content: {e}")
        return []


# Create your views here.
def index(request):
    current_language = get_language()
    
    # Get carousel items with their content
    carousel_items = []
    for item in Index.objects.filter(is_active=True).order_by('order')[:3]:
        content = IndexContent.objects.filter(index=item, language__code=current_language).first()
        if not content:
            content = IndexContent.objects.filter(index=item, language__code='en').first()
        if content:
            item.content = content
            carousel_items.append(item)
    
    # Get our approach with content
    approach_items = []
    for item in OurApproach.objects.filter(is_active=True):
        content = OurApproachContent.objects.filter(our_approach=item, language__code=current_language).first()
        if not content:
            content = OurApproachContent.objects.filter(our_approach=item, language__code='en').first()
        if content:
            item.content = content
            approach_items.append(item)
    
    # Get choose us items with content
    chooseus_items = []
    for item in ChooseUs.objects.filter(is_active=True).order_by('order'):
        content = ChooseUsContent.objects.filter(choose_us=item, language__code=current_language).first()
        if not content:
            content = ChooseUsContent.objects.filter(choose_us=item, language__code='en').first()
        if content:
            item.content = content
            chooseus_items.append(item)
    
    # Get our story with content
    our_story = None
    story_obj = OurStory.objects.filter(is_active=True).first()
    if story_obj:
        content = OurStoryContent.objects.filter(our_story=story_obj, language__code=current_language).first()
        if not content:
            content = OurStoryContent.objects.filter(our_story=story_obj, language__code='en').first()
        if content:
            story_obj.content = content
            our_story = story_obj
    
    context = {
        "queryset": carousel_items,
        "ourapp": approach_items,
        "chooseus": chooseus_items,
        "our_story": our_story,
    }
    return render(request, "index.html", context)







def contact(request):
    current_language = get_language()
    
    # Get address with content
    address = None
    address_obj = Address.objects.filter(is_active=True).first()
    if address_obj:
        content = AddressContent.objects.filter(address=address_obj, language__code=current_language).first()
        if not content:
            content = AddressContent.objects.filter(address=address_obj, language__code='en').first()
        if content:
            address_obj.content = content
            address = address_obj

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            # Save to database
            message = form.save()
            
            # Send email
            send_mail(
                subject=f"New Contact Form Submission: {message.subject}",
                message=f"""
                Name: {message.name}
                Email: {message.email}
                Subject: {message.subject}
                Message: {message.message}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],  # Your email here
                fail_silently=False,
            )

            return render(request, 'contact.html', {
                'form': ContactForm(),
                'success': True     })
    else:
        form = ContactForm()

    context={
        'form': form,
        "address" : address
    }
    
    return render(request, 'contact.html', context)


def about(request):
    current_language = get_language()
    
    clients = Clients.objects.all()
    
    # Get our approach with content
    approach_items = []
    for item in OurApproach.objects.filter(is_active=True):
        content = OurApproachContent.objects.filter(our_approach=item, language__code=current_language).first()
        if not content:
            content = OurApproachContent.objects.filter(our_approach=item, language__code='en').first()
        if content:
            item.content = content
            approach_items.append(item)
    
    # Get choose us items with content
    chooseus_items = []
    for item in ChooseUs.objects.filter(is_active=True).order_by('order'):
        content = ChooseUsContent.objects.filter(choose_us=item, language__code=current_language).first()
        if not content:
            content = ChooseUsContent.objects.filter(choose_us=item, language__code='en').first()
        if content:
            item.content = content
            chooseus_items.append(item)
    
    context = {
        "clients": clients,       
        "ourapp": approach_items,
        "chooseus": chooseus_items,
    }
    return render(request, "about.html", context)




def products(request):
    current_language = get_language()
    
    # Get main categories (parent categories) with content
    main_categories = []
    for item in ProductCategory.objects.filter(is_active=True, parent=None).order_by('order'):
        content = ProductCategoryContent.objects.filter(product_category=item, language__code=current_language).first()
        if not content:
            content = ProductCategoryContent.objects.filter(product_category=item, language__code='en').first()
        if content:
            item.content = content
            
            # Get subcategories for this main category
            subcategories = []
            for sub_item in item.subcategories.filter(is_active=True).order_by('order'):
                sub_content = ProductCategoryContent.objects.filter(product_category=sub_item, language__code=current_language).first()
                if not sub_content:
                    sub_content = ProductCategoryContent.objects.filter(product_category=sub_item, language__code='en').first()
                if sub_content:
                    sub_item.content = sub_content
                    subcategories.append(sub_item)
            
            item.subcategories_with_content = subcategories
            main_categories.append(item)
    
    # Get all categories (including subcategories) with content for filter
    all_categories = []
    for item in ProductCategory.objects.filter(is_active=True).order_by('parent__order', 'order'):
        content = ProductCategoryContent.objects.filter(product_category=item, language__code=current_language).first()
        if not content:
            content = ProductCategoryContent.objects.filter(product_category=item, language__code='en').first()
        if content:
            item.content = content
            all_categories.append(item)
    
    # Get products with content
    product_items = []
    for item in Products.objects.filter(is_active=True).order_by('order'):
        content = ProductsContent.objects.filter(product=item, language__code=current_language).first()
        if not content:
            content = ProductsContent.objects.filter(product=item, language__code='en').first()
        if content:
            item.content = content
            product_items.append(item)

    context = {
        "main_categories": main_categories,     # Ana kategoriler ve alt kategorileri
        "categories": all_categories,           # Tüm kategoriler (filtre için)
        "products": product_items,
    }
    return render(request, "portfolio.html", context)



def services(request):
    from django.http import HttpResponse
    from django.template import loader
    
    # Test template exists
    try:
        template = loader.get_template('services.html')
        html = template.render({}, request)
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"Template Error: {str(e)}")


def analytics_dashboard(request):
    # Get all time stats
    all_visitors = Visitor.objects.all()
    all_count = all_visitors.count()
    
    # Get this week's stats
    week_ago = timezone.now() - timedelta(days=7)
    week_visitors = Visitor.objects.filter(timestamp__gte=week_ago)
    week_count = week_visitors.count()
    
    # Get this month's stats
    month_ago = timezone.now() - timedelta(days=30)
    month_visitors = Visitor.objects.filter(timestamp__gte=month_ago)
    month_count = month_visitors.count()
    
    # Get this year's stats
    year_ago = timezone.now() - timedelta(days=365)
    year_visitors = Visitor.objects.filter(timestamp__gte=year_ago)
    year_count = year_visitors.count()
    
    # Get top countries
    top_countries = Visitor.objects.exclude(country__isnull=True)\
                         .values('country')\
                         .annotate(count= models.Count('country'))\
                         .order_by('-count')[:10]
    
    context = {
        'all_count': all_count,
        'week_count': week_count,
        'month_count': month_count,
        'year_count': year_count,
        'top_countries': top_countries,
    }
    
    return render(request, 'analytics/dashboard.html', context)





