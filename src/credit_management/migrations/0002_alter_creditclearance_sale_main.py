# Generated by Django 3.2 on 2022-05-11 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0015_auto_20220316_1731'),
        ('credit_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditclearance',
            name='sale_main',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='credit_clear', to='sale.salemain'),
        ),
    ]
