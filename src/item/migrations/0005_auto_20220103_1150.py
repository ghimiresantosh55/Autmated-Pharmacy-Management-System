# Generated by Django 3.1.9 on 2022-01-03 06:05

from django.db import migrations, models
import src.item.models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_item_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, upload_to='item/image', validators=[src.item.models.validate_image]),
        ),
    ]
