# Generated by Django 3.1.9 on 2022-02-18 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_order', '0011_auto_20220117_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='archived',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
    ]
