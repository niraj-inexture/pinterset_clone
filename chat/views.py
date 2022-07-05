from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from chat.models import Thread, ChatMessage


class ChatClassView(View):
    def get(self, request):
        thread_obj = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread')
        return render(request, 'chat/personal_chat.html',
                      {'thread_obj': thread_obj})


class DeleteChatClassView(View):
    def post(self, request):
        thread_id = request.POST['thread_id']
        ChatMessage.objects.filter(thread=thread_id,user=request.user.id).delete()
        return JsonResponse({'status':1})