from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
class HomeClassView(View):
    def get(self, request):
        if 'id' not in request.session:
            return redirect('login')
        return render(request, 'home/home.html')
