# Generated by Django 3.1.9 on 2022-01-07 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_auto_20220107_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.unit'),
        ),
    ]
