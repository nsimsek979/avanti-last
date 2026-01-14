from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Visitor, PageView
from .views import analytics_dashboard


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'country_display', 'city', 'page_views', 'first_visit', 'last_visit']
    list_filter = ['first_visit', 'country']
    search_fields = ['ip_address', 'country', 'city']
    readonly_fields = ['ip_address', 'session_key', 'country', 'country_code', 'city', 
                       'user_agent', 'first_visit', 'last_visit', 'page_views']
    date_hierarchy = 'first_visit'
    
    def country_display(self, obj):
        if obj.country_code:
            return format_html(
                '<span title="{}">{} {}</span>',
                obj.country or 'Unknown',
                obj.country_code,
                obj.country or ''
            )
        return obj.country or '-'
    country_display.short_description = 'Country'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(analytics_dashboard), name='analytics_dashboard'),
        ]
        return custom_urls + urls


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['url', 'visitor_ip', 'visitor_country', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['url', 'title', 'visitor__ip_address']
    readonly_fields = ['visitor', 'url', 'title', 'referrer', 'timestamp']
    date_hierarchy = 'timestamp'
    
    def visitor_ip(self, obj):
        return obj.visitor.ip_address
    visitor_ip.short_description = 'IP Address'
    
    def visitor_country(self, obj):
        return obj.visitor.country or '-'
    visitor_country.short_description = 'Country'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
