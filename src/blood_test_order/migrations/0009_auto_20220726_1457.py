# Generated by Django 3.2 on 2022-07-26 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_test', '0002_auto_20220724_1548'),
        ('blood_test_order', '0008_auto_20220726_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodtestordermain',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='default = 0.00 ', max_digits=12),
        ),
        migrations.AddField(
            model_name='bloodtestordermain',
            name='archived',
            field=models.BooleanField(default=False, help_text='By default= False'),
        ),
        migrations.AddField(
            model_name='bloodtestordermain',
            name='blood_test',
            field=models.ManyToManyField(to='blood_test.BloodTest'),
        ),
        migrations.AddField(
            model_name='bloodtestordermain',
            name='sub_total',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='default = 0.00', max_digits=12),
        ),
        migrations.AddField(
            model_name='bloodtestordermain',
            name='test_package',
            field=models.ManyToManyField(to='blood_test.TestPackage'),
        ),
        migrations.DeleteModel(
            name='BloodTestOrderDetail',
        ),
    ]