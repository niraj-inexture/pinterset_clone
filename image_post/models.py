from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone
from topic.models import Topic
from user.models import RegisterUser

# Create your models here.


IMAGE_TYPE = (
    ('Public', 'Public'),
    ('Private', 'Private'),
)


class ImageStore(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    description = models.TextField()
    image_path = CloudinaryField('image')
    approve_status = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    image_type = models.CharField(choices=IMAGE_TYPE, max_length=15)
    image_upload_date = models.DateField(default=timezone.now)


class ImageSave(models.Model):
    user = models.ForeignKey(RegisterUser,on_delete=models.CASCADE)
    image_path = models.ForeignKey(ImageStore,on_delete=models.CASCADE)
    is_save = models.BooleanField()