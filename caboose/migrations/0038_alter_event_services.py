# Generated by Django 4.0.2 on 2024-06-11 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0037_eventservice_alter_event_services_eventservice_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, through='caboose.EventService', to='caboose.Service'),
        ),
    ]