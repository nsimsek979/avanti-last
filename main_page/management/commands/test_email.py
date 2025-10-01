from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--to',
            type=str,
            help='Email address to send test email to',
            required=True
        )

    def handle(self, *args, **options):
        to_email = options['to']
        
        try:
            send_mail(
                subject='Test Email from Avanti Django App',
                message='This is a test email to verify email configuration is working correctly.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Test email sent successfully to {to_email}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Failed to send email: {str(e)}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'Please check your email configuration in .env file:\n'
                    '- EMAIL_HOST_USER: Your Gmail address\n'
                    '- EMAIL_HOST_PASSWORD: Your 16-digit App Password (not regular password)\n'
                    '- EMAIL_USE_TLS: Should be True for Gmail\n'
                    '- Make sure 2-Step Verification is enabled in your Google account'
                )
            )
