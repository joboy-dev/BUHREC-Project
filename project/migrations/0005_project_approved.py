# Generated by Django 5.0.1 on 2024-02-21 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_remove_project_figures_remove_project_tables'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
