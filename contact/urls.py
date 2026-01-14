from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='index'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter'),
]
