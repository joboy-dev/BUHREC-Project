# Generated by Django 5.0.1 on 2024-02-21 21:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_project_figures_project_tables'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='figures',
        ),
        migrations.RemoveField(
            model_name='project',
            name='tables',
        ),
    ]