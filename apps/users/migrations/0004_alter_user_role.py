# Generated by Django 4.1.2 on 2022-10-20 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_user', '0003_user_is_deleted_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('unemployed', 'Unemployed'), ('office_manager', 'Office Manager'), ('agent', 'Agent'), ('manager', 'Manager'), ('delivery', 'Delivery')], default='delivery', max_length=400, null=True),
        ),
    ]
