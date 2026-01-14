from modeltranslation.translator import translator, TranslationOptions
from .models import ContactInfo

class ContactInfoTranslationOptions(TranslationOptions):
    fields = ('address', 'working_hours')

translator.register(ContactInfo, ContactInfoTranslationOptions)
