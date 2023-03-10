# Generated by Django 3.1.9 on 2022-03-13 04:34

from django.db import migrations, models
import src.custom_lib.functions.field_value_validation


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order', '0015_auto_20220120_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorderdetail',
            name='qty',
            field=models.IntegerField(validators=[src.custom_lib.functions.field_value_validation.gt_zero_validator]),
        ),
        migrations.AlterField(
            model_name='purchaseorderreceiveddetail',
            name='qty',
            field=models.IntegerField(validators=[src.custom_lib.functions.field_value_validation.gt_zero_validator]),
        ),
    ]
