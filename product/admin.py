from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductLine)
admin.site.register(ProductBrand)
admin.site.register(Category)
admin.site.register(ProductImage)