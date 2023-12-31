# Generated by Django 4.0.2 on 2023-08-14 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0027_alter_event_grouptype'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeSubs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='recipesubs',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caboose.recipe'),
        ),
        migrations.AddField(
            model_name='recipesubs',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='caboose.recipe'),
        ),
    ]
