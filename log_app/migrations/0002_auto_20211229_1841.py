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
        ('customer', '0002_customer_user'),
        ('company', '0002_company_created_by'),
        ('purchase', '0001_initial'),
        ('purchase_order', '0001_initial'),
        ('customer_order', '0002_auto_20211229_1841'),
        ('item', '0002_auto_20211229_1841'),
        ('sale', '0001_initial'),
        ('user_group', '0001_initial'),
        ('log_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loguserpermission',
            name='category',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='foreign key to UserPermissionCategory', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user_group.userpermissioncategory'),
        ),
        migrations.AddField(
            model_name='loguser',
            name='group',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='user_group.usergroup'),
        ),
        migrations.AddField(
            model_name='logsuppliercontact',
            name='supplier',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='supplier.supplier'),
        ),
        migrations.AddField(
            model_name='logstrength',
            name='unit',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='null = true , blank = true', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.unit'),
        ),
        migrations.AddField(
            model_name='logsalemain',
            name='customer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customer.customer'),
        ),
        migrations.AddField(
            model_name='logsalemain',
            name='ref_purchase_main',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase.purchasemain'),
        ),
        migrations.AddField(
            model_name='logsalemain',
            name='ref_sale_main',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sale.salemain'),
        ),
        migrations.AddField(
            model_name='logsaledetail',
            name='item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.item'),
        ),
        migrations.AddField(
            model_name='logsaledetail',
            name='ref_purchase_detail',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase.purchasedetail'),
        ),
        migrations.AddField(
            model_name='logsaledetail',
            name='ref_sale_detail',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sale.saledetail'),
        ),
        migrations.AddField(
            model_name='logsaledetail',
            name='sale_main',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='sale.salemain'),
        ),
        migrations.AddField(
            model_name='logsaledetail',
            name='unit',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.unit'),
        ),
        migrations.AddField(
            model_name='logpurchaseordermain',
            name='customer_order_main',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customer_order.ordermain'),
        ),
        migrations.AddField(
            model_name='logpurchaseordermain',
            name='supplier',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='supplier.supplier'),
        ),
        migrations.AddField(
            model_name='logpurchaseorderdetail',
            name='customer_order_detail',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customer_order.orderdetail'),
        ),
        migrations.AddField(
            model_name='logpurchaseorderdetail',
            name='item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.item'),
        ),
        migrations.AddField(
            model_name='logpurchaseorderdetail',
            name='purchase_order_main',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase_order.purchaseordermain'),
        ),
        migrations.AddField(
            model_name='logpurchaseorderdetail',
            name='unit',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.unit'),
        ),
        migrations.AddField(
            model_name='logpurchasemain',
            name='ref_purchase',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase.purchasemain'),
        ),
        migrations.AddField(
            model_name='logpurchasemain',
            name='ref_purchase_order_main',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase_order.purchaseordermain'),
        ),
        migrations.AddField(
            model_name='logpurchasemain',
            name='supplier',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='supplier.supplier'),
        ),
        migrations.AddField(
            model_name='logpurchasedetail',
            name='item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.item'),
        ),
        migrations.AddField(
            model_name='logpurchasedetail',
            name='location',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='store.location', verbose_name='Item location'),
        ),
        migrations.AddField(
            model_name='logpurchasedetail',
            name='purchase_main',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase.purchasemain'),
        ),
        migrations.AddField(
            model_name='logpurchasedetail',
            name='ref_purchase_detail',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase.purchasedetail'),
        ),
        migrations.AddField(
            model_name='logpurchasedetail',
            name='ref_purchase_order_detail',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='purchase_order.purchaseorderdetail'),
        ),
        migrations.AddField(
            model_name='logpurchasedetail',
            name='unit',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.unit'),
        ),
        migrations.AddField(
            model_name='logproductcategory',
            name='super_category',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.supercategory'),
        ),
        migrations.AddField(
            model_name='logpopriority',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='logpopriority',
            name='supplier',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='supplier.supplier'),
        ),
        migrations.AddField(
            model_name='logordermain',
            name='customer',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customer.customer'),
        ),
        migrations.AddField(
            model_name='logordermain',
            name='delivery_person',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='null = True , blank = True, related name = delivery person', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='logorderdetail',
            name='item',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.item'),
        ),
        migrations.AddField(
            model_name='logorderdetail',
            name='order',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customer_order.ordermain'),
        ),
        migrations.AddField(
            model_name='logorderdetail',
            name='unit',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.unit'),
        ),
        migrations.AddField(
            model_name='logitem',
            name='company',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='company.company'),
        ),
        migrations.AddField(
            model_name='logitem',
            name='item_unit',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.unit'),
        ),
        migrations.AddField(
            model_name='logitem',
            name='medicine_form',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.medicineform'),
        ),
        migrations.AddField(
            model_name='logcustomer',
            name='user',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Blank= True', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]
