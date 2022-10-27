# Generated by Django 4.1.2 on 2022-10-26 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0003_order_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_seller', to=settings.AUTH_USER_MODEL),
        ),
    ]