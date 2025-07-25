# Generated by Django 5.2 on 2025-07-09 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_stock_remove_virtualstock_current_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='virtualstock',
            name='buy_price',
        ),
        migrations.RemoveField(
            model_name='virtualstock',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='virtualstock',
            name='user',
        ),
        migrations.AddField(
            model_name='virtualstock',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='virtualstock',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='virtualstock',
            name='stock',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock'),
        ),
    ]
