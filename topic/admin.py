from django.contrib import admin
from .models import Topic


# Register your models here.

class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'topic_name', 'total_likes']


admin.site.register(Topic, TopicAdmin)
