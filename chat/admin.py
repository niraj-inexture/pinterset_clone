from django.contrib import admin

# Register your models here.
from chat.models import Thread, ChatMessage
from .forms import ThreadForm

admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    model = ChatMessage


class AdminThread(admin.ModelAdmin):
    inlines = [ChatMessage]
    form = ThreadForm

    class Meta:
        model = Thread


admin.site.register(Thread, AdminThread)
