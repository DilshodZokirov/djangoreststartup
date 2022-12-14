# Generated by Django 4.0.5 on 2022-11-14 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('price', models.FloatField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product_order', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('pharmacy_name', models.CharField(blank=True, max_length=30, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=300, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('paid_price', models.FloatField(blank=True, default=0, null=True)),
                ('total_price', models.FloatField(blank=True, default=0, null=True)),
                ('paid_position', models.CharField(choices=[('not_paid', 'Not Paid'), ('orphan_paid', 'Orphan Paid'), ('full_paid', 'Full Paid')], default='not_paid', max_length=30)),
                ('order_position', models.CharField(choices=[('Pending', 'Pending'), ('Basket', 'Basket'), ('Verification', 'Verification'), ('Delivery', 'Delivery'), ('Finish', 'Finish')], default='Pending', max_length=400)),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('inn', models.CharField(blank=True, max_length=30, null=True)),
                ('products', models.ManyToManyField(related_name='order_products', to='orders.orderitem')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_seller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
