# Generated by Django 5.2 on 2025-07-12 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_userprofile_is_trading_locked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlytournamententry',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
