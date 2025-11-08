from django.contrib import admin
from apps.products.models import MeasureUnit, CategoryProduct, Indicator, Product

admin.site.register(MeasureUnit)
admin.site.register(CategoryProduct)
admin.site.register(Indicator)
admin.site.register(Product)