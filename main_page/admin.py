from django.contrib import admin
from .models import (
    Language, Index, IndexContent, OurApproach, OurApproachContent,
    ChooseUs, ChooseUsContent, ContactMessage, Clients, 
    SourcingSolutions, SourcingSolutionsContent, ConsultancyServices, ConsultancyServicesContent,
    Visitor, OurStory, OurStoryContent, ProductCategory, ProductCategoryContent, 
    Products, ProductsContent, Service, ServiceContent, Address, AddressContent,
)


# Language Admin
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']


# Index Admin with Inline Content
class IndexContentInline(admin.TabularInline):
    model = IndexContent
    extra = 1
    fields = ['language', 'carousel_header', 'carousel_line']


@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    ordering = ['order']
    inlines = [IndexContentInline]


# Our Story Admin with Inline Content
class OurStoryContentInline(admin.TabularInline):
    model = OurStoryContent
    extra = 1
    fields = ['language', 'name', 'description']


@admin.register(OurStory)
class OurStoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    inlines = [OurStoryContentInline]


# Our Approach Admin with Inline Content
class OurApproachContentInline(admin.TabularInline):
    model = OurApproachContent
    extra = 1
    fields = ['language', 'approach_header', 'approach_line']


@admin.register(OurApproach)
class OurApproachAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    inlines = [OurApproachContentInline]


# Choose Us Admin with Inline Content
class ChooseUsContentInline(admin.TabularInline):
    model = ChooseUsContent
    extra = 1
    fields = ['language', 'chooseus_header', 'chooseus_line']


@admin.register(ChooseUs)
class ChooseUsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    ordering = ['order']
    inlines = [ChooseUsContentInline]


# Sourcing Solutions Admin with Inline Content
class SourcingSolutionsContentInline(admin.TabularInline):
    model = SourcingSolutionsContent
    extra = 1
    fields = ['language', 'name', 'description']


@admin.register(SourcingSolutions)
class SourcingSolutionsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    ordering = ['order']
    inlines = [SourcingSolutionsContentInline]


# Consultancy Services Admin with Inline Content
class ConsultancyServicesContentInline(admin.TabularInline):
    model = ConsultancyServicesContent
    extra = 1
    fields = ['language', 'name', 'description']


@admin.register(ConsultancyServices)
class ConsultancyServicesAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    ordering = ['order']
    inlines = [ConsultancyServicesContentInline]


# Service Admin with Inline Content
class ServiceContentInline(admin.TabularInline):
    model = ServiceContent
    extra = 1
    fields = ['language', 'service_title', 'service_description']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    inlines = [ServiceContentInline]


# Product Category Admin with Inline Content
class ProductCategoryContentInline(admin.TabularInline):
    model = ProductCategoryContent
    extra = 1
    fields = ['language', 'name', 'description']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'parent', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['productcategory_content__name']
    list_editable = ['is_active', 'order']
    ordering = ['parent__id', 'order']
    inlines = [ProductCategoryContentInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('productcategory_content')


# Products Admin with Inline Content
class ProductsContentInline(admin.TabularInline):
    model = ProductsContent
    extra = 1
    fields = ['language', 'name']


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    ordering = ['order']
    inlines = [ProductsContentInline]


# Simple model registrations (no multi-language content)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'country', 'city', 'path', 'timestamp']
    list_filter = ['country', 'city', 'timestamp']
    readonly_fields = ['ip_address', 'user_agent', 'referrer', 'path', 'timestamp', 'country', 'city']
    ordering = ['-timestamp']


# Address Admin with Inline Content
class AddressContentInline(admin.TabularInline):
    model = AddressContent
    extra = 1
    fields = ['language', 'location', 'email', 'phone']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    fields = ['google_map', 'is_active']
    inlines = [AddressContentInline]


