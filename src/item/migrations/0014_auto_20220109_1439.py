# Generated by Django 3.1.9 on 2022-01-09 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0013_item_item_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_unit',
            field=models.ForeignKey(help_text='item unit foreign key references from ItemUnit model', on_delete=django.db.models.deletion.PROTECT, to='item.itemunit'),
        ),
    ]
