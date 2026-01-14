from django.contrib import admin
from .models import HeroSection, WhyChooseUs

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['welcome_text', 'order', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['welcome_text', 'main_heading', 'description']
    list_editable = ['order', 'is_active']

@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
