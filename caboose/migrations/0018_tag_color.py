# Generated by Django 4.0.2 on 2022-12-21 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0017_alter_event_grouptype_alter_recipe_facility_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('primary', 'Blauw'), ('secondary', 'Grijs'), ('success', 'Groen'), ('danger', 'Rood'), ('warning', 'Geel'), ('info', 'Cyaan'), ('light', 'Zwart'), ('dark', 'Wit')], default='info', max_length=20, verbose_name='Tag color'),
        ),
    ]
