# Generated by Django 4.0.2 on 2022-05-25 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0014_tag_recipe_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipeingredient',
            name='optional',
            field=models.BooleanField(default=False, verbose_name='Optional'),
        ),
    ]
