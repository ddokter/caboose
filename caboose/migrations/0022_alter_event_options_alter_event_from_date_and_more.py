# Generated by Django 4.0.2 on 2023-05-19 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0021_alter_event_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-from_date', '-to_date'], 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterField(
            model_name='event',
            name='from_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='to_date',
            field=models.DateField(),
        ),
    ]