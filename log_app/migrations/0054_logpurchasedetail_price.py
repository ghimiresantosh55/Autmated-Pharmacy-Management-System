# Generated by Django 3.1.9 on 2022-03-08 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0053_logsalepaymentdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='logpurchasedetail',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Max value  price can be upto 9999999999.99, price means MRP', max_digits=12),
        ),
    ]
