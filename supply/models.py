from django.db import models
from django.utils import timezone


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
