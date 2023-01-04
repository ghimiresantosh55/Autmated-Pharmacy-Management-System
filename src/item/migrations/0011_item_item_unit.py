# Generated by Django 3.1.9 on 2022-01-07 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0010_remove_item_item_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='item.itemunit'),
            preserve_default=False,
        ),
    ]
