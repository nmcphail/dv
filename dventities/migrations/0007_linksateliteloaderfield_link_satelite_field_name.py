# Generated by Django 2.2 on 2019-05-19 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dventities', '0006_auto_20190514_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='linksateliteloaderfield',
            name='link_satelite_field_name',
            field=models.CharField(blank=True, help_text='The satelite field that will get populated by load routines ', max_length=200),
        ),
    ]
