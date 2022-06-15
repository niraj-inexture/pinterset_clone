from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

COUNTRY_CHOICES = (
    ("India", "India"),
    ("Afghanistan", "Afghanistan"),
    ("Brazil", "Brazil"),
    ("Australia", "Australia"),
    ("Canada", "Canada"),
    ("France", "France"),
    ("Colombia", "Colombia"),
    ("Germany", "Germany"),
    ("Indonesia", "Indonesia"),
    ("Italy", "Italy"),
    ("Japan", "Japan")
)

GENDER_CHOICES = [
    ("Male", 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
]


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        abstract = True


class RegisterUser(User):
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=30)
    rejection_count = models.IntegerField(default=0)

    class Meta:
        abstract = False

    def save(self, *args, **kwargs):
        super(RegisterUser, self).save()
        img = Image.open(self.profile_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)
