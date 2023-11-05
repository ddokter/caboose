# Generated by Django 4.0.2 on 2023-11-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0031_eventingredient_event_extra_eventingredient_event_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Allergens',
                'ordering': ['name'],
            },
        ),
    ]
