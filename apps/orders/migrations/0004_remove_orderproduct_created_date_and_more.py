# Generated by Django 4.0.5 on 2022-11-14 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_inn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='updated_date',
        ),
    ]