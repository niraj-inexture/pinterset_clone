# Generated by Django 4.0.5 on 2022-06-21 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_registeruser_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registeruser',
            name='rejection_count',
        ),
    ]
