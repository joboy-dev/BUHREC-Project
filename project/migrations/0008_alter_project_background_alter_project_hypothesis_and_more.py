# Generated by Django 5.0.1 on 2024-02-21 23:46

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='background',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='', max_length=5000),
        ),
        migrations.AlterField(
            model_name='project',
            name='hypothesis',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='introduction',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='', max_length=5000),
        ),
        migrations.AlterField(
            model_name='project',
            name='justification',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='', max_length=3000),
        ),
        migrations.AlterField(
            model_name='project',
            name='literature_review',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='', max_length=10000),
        ),
        migrations.AlterField(
            model_name='project',
            name='materials_and_methods',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='', max_length=13000),
        ),
        migrations.AlterField(
            model_name='project',
            name='objectives',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='', max_length=3500),
        ),
        migrations.AlterField(
            model_name='project',
            name='procedure',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='', max_length=5000),
        ),
        migrations.AlterField(
            model_name='project',
            name='scope_and_limitation',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, default='', max_length=3000),
        ),
    ]