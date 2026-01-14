from modeltranslation.translator import translator, TranslationOptions
from .models import Story, OurApproach

class StoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

class OurApproachTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(Story, StoryTranslationOptions)
translator.register(OurApproach, OurApproachTranslationOptions)
