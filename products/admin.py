from django.contrib import admin

from .models import *
from .inlines import *


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Warehouse._meta.fields]


@admin.register(WarehouseZone)
class WarehouseZoneAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WarehouseZone._meta.fields]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]
    filter_horizontal = ('zone',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'seri_number', 'manufacturing_date',
                    'config', 'line', 'zone', 'waybill')


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'attribute', 'price',
                    'amount', 'category', 'get_cart')
    inlines = (CartProductLineInline, OrderProductLineInline)

    def get_cart(self, obj):
        return ", ".join([f'{p.cart}({p.amount})' for p in obj.cartproductline_set.all()])

    def get_order(self, obj):
        return ", ".join([f'{p.order}({p.amount}-{p.unit_price})' for p in obj.orderproductline_set.all()])


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]
    filter_horizontal = ('discountcode',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content', 'start_date',
                    'end_date', 'product_categorys')
    inlines = (EventProductCategoryInline,)

    def product_categorys(self, obj):
        return ", ".join([f'{p.category}({p.amount})' for p in obj.eventproductcategory_set.all()])


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DiscountCode._meta.fields]
    filter_horizontal = ('product_category',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_product_line')
    inlines = (CartProductLineInline,)

    def get_product_line(self, obj):
        return ", ".join([f'{p.product_line}({p.amount})' for p in obj.cartproductline_set.all()])


@admin.register(ReceiveInfo)
class ReceiveInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'receive_name', 'street',
                    'sub_district', 'district', 'city')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'payment_status', 'shipping_status',
                    'delivery_place', 'total_price', 'receive_info', 'cart',
                    'get_prodect_line')
    filter_horizontal = ('discount_code',)
    inlines = (OrderProductLineInline,)

    def get_prodect_line(self, obj):
        return ", ".join([f'{p.product_line}({p.amount}-{p.unit_price})' for p in obj.orderproductline_set.all()])


@admin.register(Waybill)
class WaybillAdmin(admin.ModelAdmin):
    list_display = ('id', 'address_type', 'delivery_time', 'transport_time',
                    'status', 'weight', 'size', 'distance', 'order', 'ship_payment', 'district')
