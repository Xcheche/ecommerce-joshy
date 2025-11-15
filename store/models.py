import django
from django.db import models
from django.core.files import File
from io import BytesIO
from PIL import Image
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    
    #Absolute url method
    def get_absolute_url(self):
        return reverse ('list_category', args=[self.slug])
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    #TODO: Migrate
    stock = models.IntegerField()
    #TODO: Migrate
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
    # method to get the thumbnail of the product
   
    def get_image_url(self):
        """Return product image URL or empty string if none."""
        if self.image:
            return self.image.url
        return ""

    def get_display_price(self):
        """Show formatted price."""
        return f"{self.price:,.2f}"