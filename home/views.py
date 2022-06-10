from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
class HomeClassView(View):
    def get(self, request):
        if 'id' not in request.session:
            return redirect('login')
        id = request.session['id']
        return render(request, 'home/home.html', {'id': id})
