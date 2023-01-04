# Generated by Django 3.1.9 on 2022-01-07 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0011_item_item_unit'),
        ('sale', '0002_auto_20211229_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saledetail',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='item.itemunit'),
        ),
    ]