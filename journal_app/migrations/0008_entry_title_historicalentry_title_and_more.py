# Generated by Django 4.2.5 on 2023-09-14 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0007_historicaltimeframe_historicallocation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='historicalentry',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalentry',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
