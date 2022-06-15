from django.contrib import admin
from .models import Topic
# Register your models here.

class TopicAdmin(admin.ModelAdmin):
    list_display = ['id','topic_name','trending_status']

admin.site.register(Topic,TopicAdmin)