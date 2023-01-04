# Generated by Django 3.2 on 2022-07-25 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0065_auto_20220725_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='logbloodtestorderdetail',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='logbloodtestorderdetail',
            name='net_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
