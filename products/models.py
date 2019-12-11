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


class Event(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        return self.name


class DicountCode(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField('start date')
    discount_type = models.IntegerField(default=0)
    discount_rate = models.FloatField()
    discount_max = models.PositiveIntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    status = models.PositiveSmallIntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class ProductLine(models.Model):
    attribute = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Product(models.Model):
    seri_number = models.CharField(max_length=200)
    manufacturing_date = models.DateTimeField('manufacturing date')
    config = models.TextField(max_length=1000)
    line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    # zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    # waybill = models.ForeignKey(Waybill, on_delete_models.CASCADE)

    def __str__(self):
        return self.seri_number
