# Generated by Django 3.1.9 on 2022-01-20 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0014_auto_20220119_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderdetail',
            name='available',
            field=models.PositiveIntegerField(choices=[(1, 'PENDING'), (2, 'RECEIVED'), (3, 'VERIFIED'), (4, 'CANCELLED')], default=1, help_text='available like pending, approved, purchased, default = 1'),
        ),
    ]