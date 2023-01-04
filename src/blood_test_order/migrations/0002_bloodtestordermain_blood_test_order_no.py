# Generated by Django 3.2 on 2022-07-25 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_test_order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodtestordermain',
            name='blood_test_order_no',
            field=models.CharField(default='hee', help_text=' Blood Test Order Id should be max. of 13 characters', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
