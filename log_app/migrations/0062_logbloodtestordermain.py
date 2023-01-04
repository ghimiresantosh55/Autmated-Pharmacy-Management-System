# Generated by Django 3.2 on 2022-07-25 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20220215_1033'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('log_app', '0061_logbloodtest_logbloodtestcategory_logtestpackage'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogBloodTestOrderMain',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('history_date_bs', models.CharField(blank=True, max_length=10, null=True)),
                ('delivery_status', models.PositiveIntegerField(choices=[(1, 'PENDING'), (2, 'CANCELLED'), (3, 'BILLED'), (4, 'PACKED'), (5, 'DISPATCHED'), (6, 'DONE'), (7, 'BILLED & PENDING')], default=1, help_text='Where 1 = PENDING, 2 = CANCELLED,  3 = BILLED,  4 = BILLED & PENDING, 5 = PACKED, 6=DISPATCHED, 7=DONE, Default=1')),
                ('amount_status', models.PositiveIntegerField(choices=[(1, 'PAID'), (2, 'UNPAID')], default=2, help_text='Where 1 = PAID, 2 = UNPAID where default = 2')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, help_text='Total  amount default=0.00', max_digits=12)),
                ('order_location', models.CharField(help_text=' Order Location should be max. of 100 characters', max_length=100)),
                ('google_location', models.CharField(blank=True, help_text=' Google Location should be max. of 100 characters', max_length=100)),
                ('remarks', models.CharField(blank=True, help_text='Remarks should be max. of 100 characters', max_length=100)),
                ('history_user_id', models.IntegerField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('customer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='customer.customer')),
                ('delivery_person', models.ForeignKey(blank=True, db_constraint=False, help_text='null = True , blank = True, related name = delivery person', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical blood test order main',
                'db_table': 'blood_test_order_blood_test_order_main_log',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]