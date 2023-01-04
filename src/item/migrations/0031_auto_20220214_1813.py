# Generated by Django 3.1.9 on 2022-02-14 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20220130_1502'),
        ('item', '0030_auto_20220211_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='items', to='company.company'),
        ),
    ]
