# Generated by Django 4.2.6 on 2023-10-31 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcrash', '0002_gameprofit_player'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameAnaylze',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_site_plus', models.CharField(max_length=100)),
                ('last_site_minus', models.CharField(max_length=100)),
            ],
        ),
    ]
