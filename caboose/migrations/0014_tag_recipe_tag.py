# Generated by Django 4.0.2 on 2022-05-24 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caboose', '0013_shipfacility_ship_facility_alter_ingredient_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(to='caboose.Tag'),
        ),
    ]
