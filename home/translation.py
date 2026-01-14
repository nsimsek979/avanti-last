from modeltranslation.translator import translator, TranslationOptions
from .models import HeroSection, WhyChooseUs

class HeroSectionTranslationOptions(TranslationOptions):
    fields = ('welcome_text', 'main_heading', 'button_text', 'button_text_2')

class WhyChooseUsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'link_text')

translator.register(HeroSection, HeroSectionTranslationOptions)
translator.register(WhyChooseUs, WhyChooseUsTranslationOptions)
