# Generated by Django 3.1.9 on 2022-01-07 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0011_item_item_unit'),
        ('customer_order', '0003_remove_orderdetail_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='item.itemunit'),
        ),
    ]
