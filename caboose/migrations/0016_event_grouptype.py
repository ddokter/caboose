# Generated by Django 4.0.2 on 2022-05-26 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0015_recipeingredient_optional'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='grouptype',
            field=models.FloatField(choices=[(0.9, '<15'), (1, 'Mixed'), (1.1, '15-25'), (0.9, '60+')], default=1, verbose_name='Group composition'),
        ),
    ]