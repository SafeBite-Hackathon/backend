# Generated by Django 5.1.3 on 2024-11-09 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0006_recipe_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
