# Generated by Django 3.1.9 on 2021-12-29 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0002_customer_user'),
        ('item', '0002_auto_20211229_1841'),
        ('sale', '0001_initial'),
        ('purchase', '0002_auto_20211229_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='salemain',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='salemain',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer.customer'),
        ),
        migrations.AddField(
            model_name='salemain',
            name='ref_purchase_main',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='purchase.purchasemain'),
        ),
        migrations.AddField(
            model_name='salemain',
            name='ref_sale_main',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sale.salemain'),
        ),
        migrations.AddField(
            model_name='saledetail',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='saledetail',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='item.item'),
        ),
        migrations.AddField(
            model_name='saledetail',
            name='ref_purchase_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='purchase.purchasedetail'),
        ),
        migrations.AddField(
            model_name='saledetail',
            name='ref_sale_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='sale.saledetail'),
        ),
        migrations.AddField(
            model_name='saledetail',
            name='sale_main',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sale_details', to='sale.salemain'),
        ),
        migrations.AddField(
            model_name='saledetail',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='item.unit'),
        ),
    ]
