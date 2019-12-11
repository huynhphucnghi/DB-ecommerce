from django.contrib import admin

from .models import Product, ProductLine, ProductCategory, Event


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'seri_number',
                    'manufacturing_date', 'config', 'line')


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'attribute', 'price')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',
                    'description', 'status', 'event')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content')
