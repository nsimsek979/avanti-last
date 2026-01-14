from django.contrib import admin
from .models import ServiceType, ServiceCategory, Service, ServiceFeature

class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'service_type', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['slug', 'category', 'is_featured', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_featured', 'category', 'created_at']
    search_fields = ['slug', 'description']
    list_editable = ['order', 'is_active', 'is_featured']
    prepopulated_fields = {'slug': ('category',)}
    inlines = [ServiceFeatureInline]
