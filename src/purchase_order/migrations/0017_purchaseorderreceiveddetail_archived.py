# Generated by Django 3.1.9 on 2022-03-13 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0016_auto_20220313_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderreceiveddetail',
            name='archived',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
    ]
