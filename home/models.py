from django.db import models

class HeroSection(models.Model):
    welcome_text = models.CharField(max_length=200, help_text='e.g., Welcome To Avanti Global')
    main_heading = models.CharField(max_length=300, help_text='e.g., Leading Sourcing And Consultancy Firm')
    image = models.ImageField(upload_to='hero/', blank=True, help_text='Hero section image')
    button_text = models.CharField(max_length=100, default='Learn More')
    button_link = models.CharField(max_length=200, default='/about/')
    button_text_2 = models.CharField(max_length=100, blank=True, help_text='Second button (optional)')
    button_link_2 = models.CharField(max_length=200, blank=True, help_text='Second button link')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Hero Section'
        verbose_name_plural = 'Hero Sections'

    def __str__(self):
        return self.welcome_text


class WhyChooseUs(models.Model):
    image = models.ImageField(upload_to='why-choose-us/', help_text='Why choose us image')
    title = models.CharField(max_length=200, help_text='e.g., Industry Expertise')
    description = models.TextField()
    link_text = models.CharField(max_length=100, default='Learn more')
    link_url = models.CharField(max_length=200, default='/about/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Why Choose Us Item'
        verbose_name_plural = 'Why Choose Us Items'

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    client_position = models.CharField(max_length=200)
    client_image = models.ImageField(upload_to='testimonials/')
    comment = models.TextField()
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"
