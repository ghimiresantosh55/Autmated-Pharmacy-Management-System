# Generated by Django 3.1.9 on 2022-01-07 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0011_item_item_unit'),
        ('log_app', '0016_auto_20220107_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='logitem',
            name='item_unit',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.itemunit'),
        ),
    ]
