# Generated by Django 3.1.9 on 2022-01-17 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0013_auto_20220117_1522'),
        ('log_app', '0030_auto_20220117_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='logpurchaseorderreceiveddetail',
            name='ref_purchase_order_received_detail',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase_order.purchaseorderreceiveddetail'),
        ),
        migrations.AddField(
            model_name='logpurchaseorderreceivedmain',
            name='ref_purchase_order_received_main',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase_order.purchaseorderreceivedmain'),
        ),
    ]
