# Generated by Django 3.1.9 on 2022-01-19 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_auto_20211229_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='pan_vat_no',
            field=models.CharField(default='1234', help_text='Pan vat no. can be max. of 10 characters', max_length=10),
            preserve_default=False,
        ),
    ]
