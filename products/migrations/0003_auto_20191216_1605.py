# Generated by Django 3.0 on 2019-12-16 16:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0001_initial'),
        ('products', '0002_auto_20191212_0318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='dicountcode',
            name='product_category',
            field=models.ManyToManyField(to='products.ProductCategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='supply.WarehouseZone'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='event',
            field=models.ManyToManyField(blank=True, through='products.EventProductCategory', to='products.Event'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('zone', models.ManyToManyField(blank=True, to='supply.WarehouseZone')),
            ],
        ),
        migrations.AddField(
            model_name='productcategory',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Category'),
        ),
    ]
