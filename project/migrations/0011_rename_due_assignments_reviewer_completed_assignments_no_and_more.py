# Generated by Django 5.0.1 on 2024-02-23 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_alter_project_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewer',
            old_name='due_assignments',
            new_name='completed_assignments_no',
        ),
        migrations.RenameField(
            model_name='reviewer',
            old_name='overdue_assignments',
            new_name='due_assignments_no',
        ),
        migrations.RenameField(
            model_name='reviewer',
            old_name='pending_assignments',
            new_name='overdue_assignments_no',
        ),
        migrations.RenameField(
            model_name='reviewer',
            old_name='withdrawn_assignments',
            new_name='pending_assignments_no',
        ),
        migrations.AddField(
            model_name='reviewer',
            name='withdrawn_assignments_no',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='reviewer',
            name='completed_assignments',
        ),
        migrations.AddField(
            model_name='reviewer',
            name='completed_assignments',
            field=models.ManyToManyField(blank=True, related_name='completed', to='project.project'),
        ),
    ]
