from django.contrib import admin
from .models import Product,ProductGallery


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','stock','category','available')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Product,ProductAdmin)
admin.site.register(ProductGallery)