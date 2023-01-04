# Generated by Django 3.1.9 on 2022-01-07 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0013_item_item_unit'),
        ('purchase_order', '0006_remove_purchaseorderdetail_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderdetail',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='item.itemunit'),
        ),
    ]
