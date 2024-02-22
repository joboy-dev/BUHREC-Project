# Generated by Django 5.0.1 on 2024-02-21 21:29

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_project_background_project_hypothesis_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='figures',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='project',
            name='tables',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=5000),
        ),
    ]