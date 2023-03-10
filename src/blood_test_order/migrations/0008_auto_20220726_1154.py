# Generated by Django 3.2 on 2022-07-26 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_test_order', '0007_auto_20220726_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloodtestorderdetail',
            name='is_blood_test',
        ),
        migrations.RemoveField(
            model_name='bloodtestorderdetail',
            name='is_test_package',
        ),
        migrations.AddField(
            model_name='bloodtestordermain',
            name='is_blood_test',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bloodtestordermain',
            name='is_test_package',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
