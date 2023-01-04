# Generated by Django 3.1.9 on 2022-04-10 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0017_purchaseorderreceiveddetail_archived'),
        ('purchase', '0015_auto_20220313_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasemain',
            name='ref_purchase_order_received_main',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='purchase_detail', to='purchase_order.purchaseorderreceivedmain'),
        ),
    ]
