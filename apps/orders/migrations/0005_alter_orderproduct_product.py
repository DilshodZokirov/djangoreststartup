# Generated by Django 4.0.5 on 2022-11-14 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_company'),
        ('orders', '0004_remove_orderproduct_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_order_product', to='product.product'),
        ),
    ]