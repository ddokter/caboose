# Generated by Django 4.0.2 on 2023-07-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0023_eventrecipe_day_eventrecipe_meal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventrecipe',
            options={'ordering': ['day', 'meal']},
        ),
        migrations.AddField(
            model_name='recipe',
            name='subs',
            field=models.ManyToManyField(blank=True, null=True, to='caboose.Recipe'),
        ),
    ]