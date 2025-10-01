from django.urls import path
from .views import index, products,   services, contact, about, analytics_dashboard

urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),   
    path("services/", services, name="services"),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
    path('analytics/', analytics_dashboard, name='analytics'),
]
