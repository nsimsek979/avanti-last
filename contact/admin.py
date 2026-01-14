from django.contrib import admin
from .models import ContactInfo, ContactMessage, Newsletter

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['phone', 'email', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    readonly_fields = ['ip_address', 'created_at', 'updated_at']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['email']
    list_editable = ['is_active']
