# Generated by Django 3.1.9 on 2022-01-09 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0014_auto_20220109_1439'),
        ('sale', '0006_auto_20220109_1050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saledetail',
            name='unit',
        ),
        migrations.AddField(
            model_name='saledetail',
            name='item_unit',
            field=models.ForeignKey(blank=True, help_text='item unit foreign key references from ItemUnit model', null=True, on_delete=django.db.models.deletion.PROTECT, to='item.itemunit'),
        ),
    ]
