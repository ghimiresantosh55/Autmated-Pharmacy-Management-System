# Generated by Django 3.1.9 on 2022-02-22 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0033_popriority_archived'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='popriority',
            unique_together=set(),
        ),
    ]