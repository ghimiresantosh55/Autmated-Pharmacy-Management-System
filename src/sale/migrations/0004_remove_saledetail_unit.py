# Generated by Django 3.1.9 on 2022-01-07 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_auto_20220107_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saledetail',
            name='unit',
        ),
    ]
