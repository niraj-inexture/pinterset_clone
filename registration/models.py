from django.db import models
from PIL import Image

# Create your models here.
COUNTRY_CHOICES = (
    ("India","India"),
    ("Afghanistan","Afghanistan"),
    ("Brazil","Brazil"),
    ("Australia","Australia"),
    ("Canada","Canada"),
    ("France","France"),
    ("Colombia","Colombia"),
    ("Germany","Germany"),
    ("Indonesia","Indonesia"),
    ("Italy","Italy"),
    ("Japan","Japan")
)

class User(models.Model):
    username = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email_id = models.EmailField(max_length=30)
    password = models.CharField(max_length=150)
    country = models.CharField(choices=COUNTRY_CHOICES,max_length=30)
    gender = models.CharField(max_length=10)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_active = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    rejection_count = models.IntegerField(default=0)

    def save(self):
        super(User, self).save()
        img = Image.open(self.profile_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)

