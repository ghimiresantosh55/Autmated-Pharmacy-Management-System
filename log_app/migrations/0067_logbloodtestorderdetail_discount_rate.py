# Generated by Django 3.2 on 2022-07-25 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0066_auto_20220725_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='logbloodtestorderdetail',
            name='discount_rate',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Discount rate  default 0.00', max_digits=12),
        ),
    ]
