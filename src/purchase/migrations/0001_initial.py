# Generated by Django 3.1.9 on 2021-12-29 12:56

from django.db import migrations, models
import src.custom_lib.functions.field_value_validation


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date_ad', models.DateTimeField()),
                ('created_date_bs', models.CharField(max_length=10)),
                ('device_type', models.PositiveBigIntegerField(choices=[(1, 'Mobile'), (2, 'PC'), (3, 'Tablet'), (4, 'Other'), (5, 'NA')], default=5, help_text='where 1=Mobile, 2=PC, 3=Tablet and 4=Other')),
                ('app_type', models.PositiveBigIntegerField(choices=[(1, 'Web-App'), (2, 'IOS-App'), (3, 'Android-App'), (4, 'NA')], default=4, help_text='where 1=Web-App, 2=IOS-APP, 3=Android-APP')),
                ('qty', models.DecimalField(decimal_places=2, max_digits=12, validators=[src.custom_lib.functions.field_value_validation.gt_zero_validator])),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, help_text='default = 0.00 ', max_digits=12)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, help_text='default = 0.00 ', max_digits=12)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseMain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date_ad', models.DateTimeField()),
                ('created_date_bs', models.CharField(max_length=10)),
                ('device_type', models.PositiveBigIntegerField(choices=[(1, 'Mobile'), (2, 'PC'), (3, 'Tablet'), (4, 'Other'), (5, 'NA')], default=5, help_text='where 1=Mobile, 2=PC, 3=Tablet and 4=Other')),
                ('app_type', models.PositiveBigIntegerField(choices=[(1, 'Web-App'), (2, 'IOS-App'), (3, 'Android-App'), (4, 'NA')], default=4, help_text='where 1=Web-App, 2=IOS-APP, 3=Android-APP')),
                ('purchase_no', models.CharField(help_text='purchase no  should be max. of 20 characters', max_length=20, unique=True)),
                ('purchase_type', models.PositiveIntegerField(choices=[(1, 'PURCHASE'), (2, 'RETURN')], help_text='Purchase type like Order, purchase, return')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, help_text='Total  amount default=0.00', max_digits=12)),
                ('remarks', models.CharField(blank=True, help_text='Remarks should be max. of 100 characters', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
