from django.contrib import admin
from .models import Category, Product

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

    search_fields = ('name',)
   
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'created_at','is_available','stock')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price','category','is_available','stock')
    search_fields = ('name', 'description')    


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)