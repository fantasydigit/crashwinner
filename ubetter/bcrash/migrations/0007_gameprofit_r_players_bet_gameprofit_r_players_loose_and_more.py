# Generated by Django 4.2.6 on 2023-11-01 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcrash', '0006_gameprofit_site_peak_valley'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameprofit',
            name='r_players_bet',
            field=models.CharField(default=0.0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameprofit',
            name='r_players_loose',
            field=models.CharField(default=0.0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameprofit',
            name='r_players_profit',
            field=models.CharField(default=0.0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameprofit',
            name='r_site_peak_valley',
            field=models.CharField(default=0.0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameprofit',
            name='r_site_profit',
            field=models.CharField(default=0.0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gameprofit',
            name='r_site_profit_sigma',
            field=models.CharField(default=0.0, max_length=100),
            preserve_default=False,
        ),
    ]
