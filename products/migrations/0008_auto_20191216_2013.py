# Generated by Django 3.0 on 2019-12-16 20:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20191216_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discountcode',
            name='discount_max',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='discount_rate',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='discount_type',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='name',
            field=models.CharField(default='Discount Code', max_length=200),
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='product_category',
            field=models.ManyToManyField(related_name='discountcode', to='products.ProductCategory'),
        ),
        migrations.AlterField(
            model_name='discountcode',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(default='Event', max_length=100),
        ),
    ]
