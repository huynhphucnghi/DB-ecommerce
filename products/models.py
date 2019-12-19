import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


WAREHOUSE_STATUS_CHOICES = (
    (1, _("Ready")),
    (2, _("Out of supply"))
)

PRODUCTS_STATUS_CHOICES = (
    (1, _("Available")),
    (2, _("Not Available"))
)


class Warehouse(models.Model):
    street = models.CharField(max_length=100, blank=True, null=True)
    sub_district = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=WAREHOUSE_STATUS_CHOICES,
                                              default=1)

    def __str__(self):
        return str(self.id)


class WarehouseZone(models.Model):
    location = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(choices=WAREHOUSE_STATUS_CHOICES,
                                              default=1)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Event(models.Model):
    name = models.CharField(default='Event', max_length=100,
                            unique=True)
    content = models.TextField(default='', max_length=1000)
    start_date = models.DateTimeField('start date', default=timezone.now)
    end_date = models.DateTimeField('end date', default=timezone.now)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=1000)
    zone = models.ManyToManyField(WarehouseZone, blank=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=200, default='Product Category',
                            unique=True)
    description = models.TextField(max_length=1000, default='No description')
    status = models.PositiveSmallIntegerField(choices=PRODUCTS_STATUS_CHOICES,
                                              default=1)
    event = models.ManyToManyField(Event, through='EventProductCategory',
                                   blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True, null=True)

    def __str__(self):
        return self.name


class EventProductCategory(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              blank=True, null=True)
    category = models.OneToOneField(ProductCategory, on_delete=models.CASCADE,
                                    blank=True, null=True)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class DiscountCode(models.Model):
    name = models.CharField(max_length=200, default='Discount Code',
                            unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    discount_type = models.PositiveSmallIntegerField(default=0)
    discount_rate = models.FloatField(default=0.0)
    discount_max = models.PositiveIntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,
                              blank=True, null=True)
    product_category = models.ManyToManyField(ProductCategory)

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    attribute = models.CharField(max_length=1000, default='No attribute')
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 null=True)

    def __str__(self):
        return str(self.id)

    @property
    def amount(self):
        return self.product_set.count()


class Cart(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              null=True, blank=True)
    product_line = models.ManyToManyField(ProductLine,
                                          through="CartProductLine")

    def __str__(self):
        return str(self.id)


class ReceiveInfo(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              null=True, blank=True)
    receive_name = models.CharField(max_length=100, blank=True,
                                    null=True, default='Ten', unique=True)
    street = models.CharField(max_length=100, blank=True,
                              null=True, default='Duong')
    sub_district = models.CharField(max_length=100, blank=True,
                                    null=True, default='Phuong')
    district = models.CharField(max_length=100, blank=True,
                                null=True, default='Quan')
    city = models.CharField(max_length=100, blank=True,
                            null=True, default='Thanh Pho')

    def __str__(self):
        return str(self.receive_name)


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now,
                                      blank=True, null=True)
    payment_status = models.PositiveSmallIntegerField(default=0,
                                                      blank=True, null=True)
    shipping_status = models.PositiveSmallIntegerField(default=0,
                                                       blank=True, null=True)
    delivery_place = models.CharField(default='Delivery Place', max_length=200,
                                      blank=True, null=True)
    receive_info = models.ForeignKey(ReceiveInfo, on_delete=models.CASCADE,
                                     blank=True, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, null=True)
    product_line = models.ManyToManyField(ProductLine,
                                          through="OrderProductLine")
    discount_code = models.ManyToManyField(DiscountCode, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        obj_set = self.orderproductline_set.all()
        return obj_set.aggregate(total_price=models.Sum(models.F('amount')*models.F('unit_price'))).get('total_price')


class Waybill(models.Model):
    address_type = models.PositiveSmallIntegerField(default=0)
    delivery_time = models.DateTimeField(default=timezone.now)
    transport_time = models.DateTimeField(default=timezone.now)
    status = models.PositiveSmallIntegerField(default=0)
    weight = models.FloatField(default=0.0)
    size = models.CharField(max_length=100, default=0)
    distance = models.FloatField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def ship_payment(self):
        coef = 1500
        return int(coef*self.distance)

    @property
    def district(self):
        return self.order.receive_info.district


class Product(models.Model):
    seri_number = models.CharField(max_length=200, default='Product',
                                   unique=True)
    manufacturing_date = models.DateTimeField(default=timezone.now)
    config = models.TextField(max_length=1000, default='No config')
    line = models.ForeignKey(ProductLine, on_delete=models.CASCADE,
                             null=True)
    zone = models.ForeignKey(WarehouseZone, on_delete=models.CASCADE,
                             null=True)
    waybill = models.ForeignKey(Waybill, on_delete=models.CASCADE,
                                blank=True, null=True)

    def __str__(self):
        return self.seri_number


class Review(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              null=True, blank=True)
    content = models.TextField(default='', max_length=1000)
    point = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    @property
    def liked(self):
        # TODO:
        return 0


class Write(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                 null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               blank=True, null=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.SET_NULL,
                                     blank=True, null=True)

    def __str__(self):
        return str(self.id)


class CartProductLine(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             null=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE,
                                     blank=True, null=True)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


class OrderProductLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              null=True, blank=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE,
                                     null=True, blank=True)
    amount = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField(default=1000)

    def __str__(self):
        return str(self.id)
