import datetime

from django.db import models
from django.utils import timezone


# STATUS_CHOICES = (
#     (1, _("Not relevant")),
#     (2, _("Review")),
#     (3, _("Maybe relevant")),
#     (4, _("Relevant")),
#     (5, _("Leading candidate"))
# )


class Warehouse(models.Model):
    street = models.CharField(max_length=100, blank=True, null=True)
    sub_district = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    status = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.id)


class WarehouseZone(models.Model):
    status = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=100)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Event(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(default='', max_length=1000)
    start_date = models.DateTimeField('start date', default=timezone.now)
    end_date = models.DateTimeField('end date', default=timezone.now)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    zone = models.ManyToManyField(WarehouseZone, blank=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    status = models.PositiveSmallIntegerField(default=0)
    event = models.ManyToManyField(Event, through='EventProductCategory',
                                   blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True, null=True)

    def __str__(self):
        return self.name


class DiscountCode(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField('start date')
    discount_type = models.IntegerField(default=0)
    discount_rate = models.FloatField()
    discount_max = models.PositiveIntegerField()
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, blank=True, null=True)
    product_category = models.ManyToManyField(ProductCategory)

    def __str__(self):
        return self.name


class ProductLine(models.Model):
    attribute = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    # TODO:account
    product_line = models.ManyToManyField(ProductLine,
                                          through="CartProductLine")

    def __str__(self):
        return str(self.id)


class ReceiveInfo(models.Model):
    # TODO:account
    receive_name = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    sub_district = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    payment_status = models.PositiveSmallIntegerField(default=0)
    shipping_status = models.PositiveSmallIntegerField(default=0)
    delivery_place = models.CharField(default='', max_length=200)
    # TODO:total_payment
    receive_info = models.ForeignKey(ReceiveInfo, on_delete=models.CASCADE,
                                     blank=True, null=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, blank=True,
                                null=True)
    product_line = models.ManyToManyField(ProductLine,
                                          through="OrderProductLine")
    discount_code = models.ManyToManyField(DiscountCode, blank=True)

    def __str__(self):
        return str(self.id)


class Waybill(models.Model):
    address_type = models.PositiveSmallIntegerField()
    delivery_time = models.DateTimeField(default=timezone.now)
    transport_time = models.DateTimeField(default=timezone.now)
    status = models.PositiveSmallIntegerField()
    weight = models.FloatField()
    size = models.CharField(max_length=100)
    distance = models.FloatField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def ship_payment(self):
        # TODO:
        return 0

    @property
    def district(self):
        # TODO:
        return 0


class Product(models.Model):
    seri_number = models.CharField(max_length=200)
    manufacturing_date = models.DateTimeField('manufacturing date')
    config = models.TextField(max_length=1000)
    line = models.ForeignKey(ProductLine, on_delete=models.CASCADE,
                             blank=True, null=True)
    zone = models.ForeignKey(WarehouseZone, on_delete=models.CASCADE,
                             blank=True, null=True)
    waybill = models.ForeignKey(Waybill, on_delete=models.CASCADE,
                                blank=True, null=True)

    def __str__(self):
        return self.seri_number


class EventProductCategory(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE,
                                 blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,
                                 blank=True, null=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class Review(models.Model):
    # account
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
    # account
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               blank=True, null=True)
    product_line = models.OneToOneField(ProductLine, on_delete=models.SET_NULL,
                                        blank=True, null=True)

    def __str__(self):
        return str(self.id)


class CartProductLine(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True,
                             null=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE,
                                     blank=True, null=True)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class OrderProductLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              blank=True)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE,
                                     blank=True, null=True)
    amount = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)
