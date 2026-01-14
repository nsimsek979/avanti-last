from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory

def product_list(request):
    categories = ProductCategory.objects.filter(is_active=True).prefetch_related('products')
    
    context = {
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {
        'product': product,
        'related_products': Product.objects.filter(
            category=product.category, 
            is_active=True
        ).exclude(id=product.id)[:4],
    }
    return render(request, 'products/product_detail.html', context)
