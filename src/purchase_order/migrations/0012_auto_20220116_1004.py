# Generated by Django 3.1.9 on 2022-01-16 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0011_auto_20220113_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorderreceivedmain',
            old_name='purchase_receive_order_type',
            new_name='purchase_order_receive_type',
        ),
    ]
