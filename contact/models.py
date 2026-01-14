from django.db import models

class ContactInfo(models.Model):
    company_name = models.CharField(max_length=200, default='AVANTI GLOBAL SRL')
    logo = models.ImageField(upload_to='company/', blank=True, null=True, help_text='Company logo')
    address = models.TextField(help_text='Full address with postal code')
    city = models.CharField(max_length=100, default='București')
    sector = models.CharField(max_length=50, default='Sectorul 6', blank=True)
    country = models.CharField(max_length=100, default='Romania')
    phone = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    email2 = models.EmailField(blank=True)
    working_hours = models.TextField(blank=True)
    map_embed = models.TextField(blank=True, help_text='Google Maps embed code')
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Information'
        verbose_name_plural = 'Contact Information'

    def __str__(self):
        return self.company_name


class ContactMessage(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    )
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'

    def __str__(self):
        return self.email
