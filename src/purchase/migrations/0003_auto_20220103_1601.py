# Generated by Django 3.1.9 on 2022-01-03 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_auto_20211229_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasemain',
            name='purchase_type',
            field=models.PositiveIntegerField(choices=[(1, 'PURCHASE'), (2, 'RETURN'), (3, 'OPENING-STOCK')], help_text='Purchase type like  purchase, return, opening stock'),
        ),
    ]
