# Generated by Django 3.0.8 on 2020-10-19 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definitions', '0018_auto_20201015_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='readme',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='table',
            name='readme',
            field=models.TextField(blank=True, null=True),
        ),
    ]
