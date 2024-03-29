# Generated by Django 5.0.1 on 2024-02-23 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_remove_reviewer_assignments_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='payment_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='track_id',
            field=models.UUIDField(null=True, unique=True),
        ),
    ]
