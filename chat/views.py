from django.shortcuts import render

# Create your views here.
from django.views import View

from chat.models import Thread


class ChatClassView(View):
    def get(self, request):
        thread_obj = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
        return render(request, 'chat/personal_chat.html',
                      {'thread_obj': thread_obj})
