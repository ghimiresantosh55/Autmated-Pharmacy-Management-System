# Generated by Django 3.1.9 on 2022-01-07 05:48

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_auto_20220107_1133'),
        ('log_app', '0009_auto_20220103_1936'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogItemUnit',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('history_date_bs', models.CharField(blank=True, max_length=10, null=True)),
                ('device_type', models.PositiveBigIntegerField(choices=[(1, 'Mobile'), (2, 'PC'), (3, 'Tablet'), (4, 'Other'), (5, 'NA')], default=5, help_text='where 1=Mobile, 2=PC, 3=Tablet and 4=Other')),
                ('app_type', models.PositiveBigIntegerField(choices=[(1, 'Web-App'), (2, 'IOS-App'), (3, 'Android-App'), (4, 'NA')], default=4, help_text='where 1=Web-App, 2=IOS-APP, 3=Android-APP')),
                ('name', models.CharField(db_index=True, help_text=' Product Unit name can be max. of 50 characters and must be unique', max_length=50)),
                ('short_form', models.CharField(db_index=True, help_text='short_form can be max. of 20 characters and must be unique', max_length=20)),
                ('display_order', models.IntegerField(blank=True, default=0, help_text='Display order for ordering, default=0,blank= True, null= True', null=True)),
                ('active', models.BooleanField(default=True, help_text='By default active=True')),
                ('history_user_id', models.IntegerField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical product unit',
                'db_table': 'item_product_Unit_log',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AlterField(
            model_name='logitem',
            name='item_unit',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='item.ItemUnit'),
        ),
    ]
