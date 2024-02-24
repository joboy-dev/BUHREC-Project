# Generated by Django 5.0.1 on 2024-02-23 17:45

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_project_payment_approved_project_track_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('message', models.TextField(max_length=1000)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('reviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.reviewer')),
            ],
        ),
    ]