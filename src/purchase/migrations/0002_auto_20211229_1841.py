# Generated by Django 3.1.9 on 2021-12-29 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('supplier', '0001_initial'),
        ('store', '0001_initial'),
        ('purchase', '0001_initial'),
        ('purchase_order', '0001_initial'),
        ('item', '0002_auto_20211229_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasemain',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchasemain',
            name='ref_purchase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='purchase.purchasemain'),
        ),
        migrations.AddField(
            model_name='purchasemain',
            name='ref_purchase_order_main',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='purchase_order.purchaseordermain'),
        ),
        migrations.AddField(
            model_name='purchasemain',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='supplier.supplier'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.item'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='store.location', verbose_name='Item location'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='purchase_main',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchase_details', to='purchase.purchasemain'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='ref_purchase_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='purchase.purchasedetail'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='ref_purchase_order_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='purchase_order.purchaseorderdetail'),
        ),
        migrations.AddField(
            model_name='purchasedetail',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='item.unit'),
        ),
    ]
