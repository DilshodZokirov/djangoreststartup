# Generated by Django 4.0.5 on 2022-12-11 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_user', '0013_alter_user_phone_number_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('unemployed', 'Unemployed'), ('office_manager', 'Office Manager'), ('agent', 'Agent'), ('manager', 'Manager'), ('delivery', 'Delivery')], default='delivery', max_length=400, null=True),
        ),
    ]
