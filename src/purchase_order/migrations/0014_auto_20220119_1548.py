# Generated by Django 3.1.9 on 2022-01-19 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0013_auto_20220117_1522'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorderreceivedmain',
            old_name='purchase_receive_no',
            new_name='purchase_order_received_no',
        ),
        migrations.RenameField(
            model_name='purchaseorderreceivedmain',
            old_name='purchase_order_receive_type',
            new_name='purchase_order_received_type',
        ),
    ]
