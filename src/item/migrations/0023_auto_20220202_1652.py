# Generated by Django 3.1.9 on 2022-02-02 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0022_auto_20220202_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genericstrength',
            name='app_type',
        ),
        migrations.RemoveField(
            model_name='genericstrength',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='genericstrength',
            name='created_date_ad',
        ),
        migrations.RemoveField(
            model_name='genericstrength',
            name='created_date_bs',
        ),
        migrations.RemoveField(
            model_name='genericstrength',
            name='device_type',
        ),
    ]
