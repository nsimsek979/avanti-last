from modeltranslation.translator import translator, TranslationOptions
from .models import ProductCategory, Product, ProductSpecification

class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class ProductSpecificationTranslationOptions(TranslationOptions):
    fields = ('name', 'value')

translator.register(ProductCategory, ProductCategoryTranslationOptions)
translator.register(Product, ProductTranslationOptions)
translator.register(ProductSpecification, ProductSpecificationTranslationOptions)
