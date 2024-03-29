# Generated by Django 5.0.1 on 2024-02-23 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_customuser_payment_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='role',
            field=models.CharField(choices=[('chair', 'Chair'), ('asst chair', 'Assistant chair'), ('staff', 'Staff')], default='staff', max_length=10),
        ),
    ]
