# Generated by Django 4.0.5 on 2022-11-12 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_user', '0016_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('unemployed', 'Unemployed'), ('office_manager', 'Office Manager'), ('agent', 'Agent'), ('manager', 'Manager'), ('delivery', 'Delivery')], default='delivery', max_length=400, null=True),
        ),
    ]