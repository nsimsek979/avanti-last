from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Multi-language content models
class Language(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Language Code"))
    name = models.CharField(max_length=50, verbose_name=_("Language Name"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")


class MultiLanguageContent(models.Model):
    """Base model for multi-language content"""
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name=_("Language"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Index(models.Model):
    image = models.ImageField(upload_to="carousal-image", verbose_name=_("Carrousel Images"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # Get the first available translation
        first_content = self.index_content.first()
        return first_content.carousel_header if first_content else f"Carousel #{self.id}"

    class Meta:
        verbose_name = _("Carrousel")
        verbose_name_plural = _("Carrousels")
        ordering = ['order']


class IndexContent(MultiLanguageContent):
    index = models.ForeignKey(Index, on_delete=models.CASCADE, related_name='index_content')
    carousel_header = models.CharField(max_length=150, verbose_name=_("Carrousel Header"))
    carousel_line = models.CharField(max_length=300, verbose_name=_("Carrousel Description"))
    
    def __str__(self):
        return f"{self.carousel_header} ({self.language.code})"
    
    class Meta:
        verbose_name = _("Carrousel Content")
        verbose_name_plural = _("Carrousel Contents")
        unique_together = ['index', 'language']

class OurStory(models.Model):
    image = models.ImageField(upload_to="OurStory", verbose_name=_("Images"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_content = self.ourstory_content.first()
        return first_content.name if first_content else f"Our Story #{self.id}"
    
    class Meta:
        verbose_name = _("Our Story")
        verbose_name_plural = _("Our Story")


class OurStoryContent(MultiLanguageContent):
    our_story = models.ForeignKey(OurStory, on_delete=models.CASCADE, related_name='ourstory_content')
    name = models.CharField(max_length=50, verbose_name=_("Title"))
    description = models.TextField(max_length=1000, verbose_name=_("Description"))
    
    def __str__(self):
        return f"{self.name} ({self.language.code})"
    
    class Meta:
        verbose_name = _("Our Story Content")
        verbose_name_plural = _("Our Story Contents")
        unique_together = ['our_story', 'language']


class OurApproach(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        first_content = self.ourapproach_content.first()
        return first_content.approach_header if first_content else f"Our Approach #{self.id}"
    
    class Meta:
        verbose_name = _("Our Approach")
        verbose_name_plural = _("Our Approaches")


class OurApproachContent(MultiLanguageContent):
    our_approach = models.ForeignKey(OurApproach, on_delete=models.CASCADE, related_name='ourapproach_content')
    approach_header = models.CharField(max_length=150, verbose_name=_("Our Approach"))
    approach_line = models.TextField(max_length=1000, verbose_name=_("Our Approach Description"))
    
    def __str__(self):
        return f"{self.approach_header} ({self.language.code})"
    
    class Meta:
        verbose_name = _("Our Approach Content")
        verbose_name_plural = _("Our Approach Contents")
        unique_together = ['our_approach', 'language']

class ChooseUs(models.Model):
    image = models.ImageField(upload_to="chooseus-image", verbose_name=_("Images"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        first_content = self.chooseus_content.first()
        return first_content.chooseus_header if first_content else f"Choose Us #{self.id}"
    
    class Meta:
        verbose_name = _("Why Us")  
        verbose_name_plural = _("Why Us")
        ordering = ['order']


class ChooseUsContent(MultiLanguageContent):
    choose_us = models.ForeignKey(ChooseUs, on_delete=models.CASCADE, related_name='chooseus_content')
    chooseus_header = models.CharField(max_length=150, verbose_name=_("Why Us"))
    chooseus_line = models.CharField(max_length=300, verbose_name=_("Why Us Description"))
    
    def __str__(self):
        return f"{self.chooseus_header} ({self.language.code})"
    
    class Meta:
        verbose_name = _("Why Us Content")
        verbose_name_plural = _("Why Us Contents")
        unique_together = ['choose_us', 'language']
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']

class Clients (models.Model):
    name = models.CharField(max_length=100, verbose_name="Client Name")
    image = models.ImageField( upload_to="client-image", verbose_name="Client Logo")
    created_at = models.DateTimeField( auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Client")  
        verbose_name_plural = _("Clients")

class SourcingSolutions(models.Model):
    image = models.ImageField(upload_to="sourcing-solution", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        first_content = self.sourcingsolutions_content.first()
        return first_content.name if first_content else f"Sourcing Solution #{self.id}"
        
    class Meta:
        verbose_name = _("Sourcing Solution")
        verbose_name_plural = _("Sourcing Solutions")
        ordering = ['order']


class SourcingSolutionsContent(MultiLanguageContent):
    sourcing_solution = models.ForeignKey(SourcingSolutions, on_delete=models.CASCADE, related_name='sourcingsolutions_content')
    name = models.CharField(max_length=100, verbose_name=_("Sourcing Solutions"))
    description = models.TextField(max_length=500, verbose_name=_("Description"))
    
    def __str__(self):
        return f"{self.name} ({self.language.code})"
        
    class Meta:
        verbose_name = _("Sourcing Solution Content")
        verbose_name_plural = _("Sourcing Solution Contents")
        unique_together = ['sourcing_solution', 'language']


class ConsultancyServices(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_content = self.consultancyservices_content.first()
        return first_content.name if first_content else f"Consultancy Service #{self.id}"

    class Meta:
        verbose_name = _("Consultancy Service")
        verbose_name_plural = _("Consultancy Services")
        ordering = ['order']


class ConsultancyServicesContent(MultiLanguageContent):
    consultancy_service = models.ForeignKey(ConsultancyServices, on_delete=models.CASCADE, related_name='consultancyservices_content')
    name = models.CharField(max_length=100, verbose_name=_("Consultancy Services"))
    description = models.TextField(max_length=1000, verbose_name=_("Description"))
    
    def __str__(self):
        return f"{self.name} ({self.language.code})"
        
    class Meta:
        verbose_name = _("Consultancy Service Content")
        verbose_name_plural = _("Consultancy Service Contents")
        unique_together = ['consultancy_service', 'language']
    
class Service(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_content = self.service_content.first()
        return first_content.service_description[:50] if first_content else f"Service #{self.id}"

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class ServiceContent(MultiLanguageContent):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_content')
    service_title = models.CharField(max_length=100, verbose_name=_("Service Title"))
    service_description = models.TextField(verbose_name=_("Services"))
    
    def __str__(self):
        return f"{self.service_description[:50]}... ({self.language.code})"
        
    class Meta:
        verbose_name = _("Service Content")
        verbose_name_plural = _("Service Contents")
        unique_together = ['service', 'language']


class ProductCategory(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name=_("Parent Category"))
    image = models.ImageField(upload_to="category", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_content = self.productcategory_content.first()
        return first_content.name if first_content else f"Category #{self.id}"
    
    @property
    def is_parent(self):
        return self.parent is None
    
    @property
    def is_subcategory(self):
        return self.parent is not None
    
    def get_all_subcategories(self):
        """Tüm alt kategorileri döndürür"""
        return self.subcategories.filter(is_active=True).order_by('order')
    
    def get_products(self):
        """Bu kategoriye ait ürünleri döndürür"""
        return self.products.filter(is_active=True)

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")
        ordering = ['parent__id', 'order', 'id']


class ProductCategoryContent(MultiLanguageContent):
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='productcategory_content')
    name = models.CharField(max_length=100, verbose_name=_("Category"))
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name=_("Description"))
    
    def __str__(self):
        return f"{self.name} ({self.language.code})"
        
    class Meta:
        verbose_name = _("Product Category Content")
        verbose_name_plural = _("Product Category Contents")
        unique_together = ['product_category', 'language']

class Products(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    order = models.IntegerField(default=0, verbose_name=_("Order"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_content = self.products_content.first()
        return first_content.name if first_content else f"Product #{self.id}"

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['order']


class ProductsContent(MultiLanguageContent):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='products_content')
    name = models.CharField(max_length=100, verbose_name=_("Products"))
    
    def __str__(self):
        return f"{self.name} ({self.language.code})"
        
    class Meta:
        verbose_name = _("Product Content")
        verbose_name_plural = _("Product Contents")
        unique_together = ['product', 'language']

class Address(models.Model):
    google_map = models.CharField(max_length=850, verbose_name=_("Google Map"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_content = self.address_content.first()
        return first_content.location if first_content else f"Address #{self.id}"

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")


class AddressContent(MultiLanguageContent):
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_content')
    location = models.CharField(max_length=350, verbose_name=_("Location"))
    email = models.CharField(max_length=50, verbose_name=_("Email"))
    phone = models.CharField(max_length=50, verbose_name=_("Phone"))
    
    def __str__(self):
        return f"{self.location} ({self.language.code})"
        
    class Meta:
        verbose_name = _("Address Content")
        verbose_name_plural = _("Address Contents")
        unique_together = ['address', 'language']


# models.py

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name=_("IP Address"))
    user_agent = models.TextField(null=True, blank=True, verbose_name=_("User Agent"))
    referrer = models.URLField(null=True, blank=True, verbose_name=_("Referrer"))
    path = models.CharField(max_length=255, verbose_name=_("Path"))
    timestamp = models.DateTimeField(default=timezone.now, verbose_name=_("Timestamp"))
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Country"))
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("City"))

    class Meta:
        ordering = ['-timestamp']