# Generated by Django 4.0.2 on 2022-04-26 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0004_recipe_descr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='avg_pp',
            field=models.FloatField(blank=True, null=True, verbose_name='Average per person'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='descr',
            field=models.CharField(max_length=200, verbose_name='Description'),
        ),
    ]
