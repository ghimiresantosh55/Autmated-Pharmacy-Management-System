# Generated by Django 3.2 on 2022-07-25 10:38

from django.db import migrations, models
import src.custom_lib.functions.field_value_validation


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0064_logbloodtestorderdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logbloodtestorderdetail',
            name='net_amount',
        ),
        migrations.AddField(
            model_name='logbloodtestorderdetail',
            name='qty',
            field=models.IntegerField(default=2, validators=[src.custom_lib.functions.field_value_validation.gt_zero_validator]),
            preserve_default=False,
        ),
    ]
