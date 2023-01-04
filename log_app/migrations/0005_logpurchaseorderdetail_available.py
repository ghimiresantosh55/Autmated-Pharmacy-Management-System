# Generated by Django 3.1.9 on 2022-01-02 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0004_logitem_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='logpurchaseorderdetail',
            name='available',
            field=models.PositiveIntegerField(choices=[(1, 'PENDING'), (2, 'PURCHASED'), (3, 'APPROVED')], default=1, help_text='available like pending, approved, purchased, default = 1'),
        ),
    ]