from modeltranslation.translator import translator, TranslationOptions
from .models import ServiceType, ServiceCategory, Service, ServiceFeature

class ServiceTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class ServiceCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class ServiceTranslationOptions(TranslationOptions):
    fields = ('short_description', 'description', 'price_info')

class ServiceFeatureTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(ServiceType, ServiceTypeTranslationOptions)
translator.register(ServiceCategory, ServiceCategoryTranslationOptions)
translator.register(Service, ServiceTranslationOptions)
translator.register(ServiceFeature, ServiceFeatureTranslationOptions)
