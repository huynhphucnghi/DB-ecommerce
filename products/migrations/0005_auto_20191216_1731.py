# Generated by Django 3.0 on 2019-12-16 17:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20191216_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiveInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receive_name', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_district', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_district', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='review',
            name='amount',
        ),
        migrations.AddField(
            model_name='review',
            name='content',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='event',
            name='content',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.CreateModel(
            name='Write',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_line', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductLine')),
                ('review', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Review')),
            ],
        ),
        migrations.CreateModel(
            name='Waybill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.PositiveSmallIntegerField()),
                ('delivery_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('transport_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.PositiveSmallIntegerField()),
                ('weight', models.FloatField()),
                ('size', models.CharField(max_length=100)),
                ('distance', models.FloatField()),
                ('order', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='products.Order')),
            ],
        ),
        migrations.CreateModel(
            name='WarehouseZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField()),
                ('location', models.CharField(max_length=100)),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.Warehouse')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='receive_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.ReceiveInfo'),
        ),
        migrations.AlterField(
            model_name='category',
            name='zone',
            field=models.ManyToManyField(blank=True, to='products.WarehouseZone'),
        ),
        migrations.AlterField(
            model_name='product',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.WarehouseZone'),
        ),
    ]
