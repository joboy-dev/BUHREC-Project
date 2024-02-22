# Generated by Django 5.0.1 on 2024-02-21 21:16

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='background',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='project',
            name='hypothesis',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='introduction',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='project',
            name='justification',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=3000),
        ),
        migrations.AddField(
            model_name='project',
            name='literature_review',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=10000),
        ),
        migrations.AddField(
            model_name='project',
            name='materials_and_methods',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=13000),
        ),
        migrations.AddField(
            model_name='project',
            name='objectives',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=3500),
        ),
        migrations.AddField(
            model_name='project',
            name='procedure',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='project',
            name='scope_and_limitation',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', max_length=3000),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]