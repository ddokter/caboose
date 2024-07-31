# Generated by Django 4.0.2 on 2024-06-11 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0035_alter_tag_color_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),        
        migrations.RemoveField(
            model_name='service',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='services',
            field=models.ManyToManyField(through='caboose.EventService', to='caboose.Service'),
        ),

    ]
