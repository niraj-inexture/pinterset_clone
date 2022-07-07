from django.contrib import admin
from .models import ImageStore, ImageSave, ImageLike, Comment, BoardImages


# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'description', 'image_path', 'image_type', 'approve_status',
        'image_upload_date')


admin.site.register(ImageStore, ImageAdmin)


class ImageSaveAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_id', 'image_path', 'is_save')


admin.site.register(ImageSave, ImageSaveAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id','user', 'image_path', 'comment')


admin.site.register(Comment, CommentAdmin)


class ImageLikeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'like_user')


admin.site.register(ImageLike, ImageLikeAdmin)


class BoardImagesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'topic', 'image_post')


admin.site.register(BoardImages, BoardImagesAdmin)