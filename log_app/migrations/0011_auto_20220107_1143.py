# Generated by Django 3.1.9 on 2022-01-07 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0007_auto_20220107_1143'),
        ('log_app', '0010_auto_20220107_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logitem',
            name='item_unit',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.unit'),
        ),
    ]
