# Generated by Django 3.1.9 on 2022-02-02 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0020_item_generic_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='generic_name',
            field=models.ManyToManyField(blank=True, to='item.GenericStrength'),
        ),
    ]
