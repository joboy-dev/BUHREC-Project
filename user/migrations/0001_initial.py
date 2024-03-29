# Generated by Django 5.0.1 on 2024-02-21 11:47

import django.db.models.deletion
import user.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('profile_pic', models.ImageField(default='default.png', null=True, upload_to=user.models.CustomUser.upload_image)),
                ('role', models.CharField(choices=[('student', 'Student'), ('researcher', 'Researcher'), ('reviewer', 'Reviewer'), ('admin', 'Admin')], default='student', max_length=10)),
                ('payment_approved', models.BooleanField(default=False)),
                ('track_no', models.IntegerField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentOrResearcher',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('degree', models.CharField(choices=[('undergraduate', 'Undergraduate'), ('postgraduate', 'Postgraduate'), ('independent', 'Independent')], default='undergraduate', max_length=13)),
                ('pg_degree', models.CharField(choices=[('phd', 'PhD'), ('msc', 'MSc'), ('pgd', 'PGD')], max_length=3, null=True)),
                ('programme', models.CharField(choices=[('computer science', 'Computer Science'), ('environmental science', 'Environmental Science'), ('science', 'Science'), ('health', 'Health'), ('mamagement', 'Management'), ('humanities', 'Humanities')], default='science', max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('country_domicile', models.CharField(max_length=72)),
                ('institution_name', models.CharField(max_length=72)),
                ('years_of_reviewing', models.IntegerField(default=0)),
                ('pending_assignments', models.IntegerField(default=0)),
                ('completed_assignments', models.IntegerField(default=0)),
                ('due_assignments', models.IntegerField(default=0)),
                ('overdue_assignments', models.IntegerField(default=0)),
                ('withdrawn_assignments', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('assignments', models.ManyToManyField(blank=True, related_name='students', to='user.studentorresearcher')),
            ],
        ),
    ]
