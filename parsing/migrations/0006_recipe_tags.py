# Generated by Django 5.1.3 on 2024-11-09 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0005_recipe_active_time_recipe_prep_time_recipe_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='parsing.tag'),
        ),
    ]
