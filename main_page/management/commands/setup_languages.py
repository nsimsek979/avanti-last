from django.core.management.base import BaseCommand
from main_page.models import Language


class Command(BaseCommand):
    help = 'Create initial languages for the multi-language site'

    def handle(self, *args, **options):
        languages = [
            {'code': 'en', 'name': 'English'},
            {'code': 'tr', 'name': 'Türkçe'},
            {'code': 'ro', 'name': 'Română'},
        ]

        for lang_data in languages:
            language, created = Language.objects.get_or_create(
                code=lang_data['code'],
                defaults={'name': lang_data['name']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created language: {language.name} ({language.code})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Language already exists: {language.name} ({language.code})')
                )

        self.stdout.write(self.style.SUCCESS('Language setup completed!'))
