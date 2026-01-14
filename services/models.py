from django.db import models

class ServiceType(models.Model):
    name = models.CharField(max_length=100, help_text='e.g., Sourcing Solutions, Consultancy Services')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, help_text='Font Awesome icon class', blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service Type'
        verbose_name_plural = 'Service Types'

    def __str__(self):
        return self.name


class ServiceCategory(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='services/categories/', blank=True, help_text='Category image')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    slug = models.SlugField(unique=True)
    short_description = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
    icon = models.CharField(max_length=100, help_text='Font Awesome icon class')
    price_info = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.slug


class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text='Font Awesome icon class', blank=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service Feature'
        verbose_name_plural = 'Service Features'

    def __str__(self):
        return f"{self.service.title} - {self.title}"
