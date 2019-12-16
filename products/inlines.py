from django.contrib import admin

from .models import *


class EventProductCategoryInline(admin.TabularInline):
    model = EventProductCategory
    extra = 1


class CartProductLineInline(admin.TabularInline):
    model = CartProductLine
    extra = 1


class OrderProductLineInline(admin.TabularInline):
    model = OrderProductLine
    extra = 1
