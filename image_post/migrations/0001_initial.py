# Generated by Django 4.0.5 on 2022-06-23 11:32

import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ImageSave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_save', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ImageStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('image_path', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('approve_status', models.BooleanField(default=False)),
                ('like_count', models.IntegerField(default=0)),
                ('image_type', models.CharField(choices=[('Public', 'Public'), ('Private', 'Private')], max_length=15)),
                ('image_upload_date', models.DateField(default=django.utils.timezone.now)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topic.topic')),
            ],
        ),
    ]
