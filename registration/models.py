from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email_id = models.EmailField(max_length=30)
    password = models.CharField(max_length=150)
    country = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_active = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    rejection_count = models.IntegerField(default=0)



