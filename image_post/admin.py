from django.contrib import admin
from .models import ImageStore, ImageSave


# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'topic_id', 'description', 'image_path', 'image_type', 'like_count', 'approve_status',
        'image_upload_date')


admin.site.register(ImageStore, ImageAdmin)


class ImageSaveAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'image_path', 'is_save')


admin.site.register(ImageSave,ImageSaveAdmin)
