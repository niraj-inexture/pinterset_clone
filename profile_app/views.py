from django.shortcuts import render, redirect
from django.views import View
from .forms import ProfileUpdateForm
from registration.models import User
from django.contrib import messages
# Create your views here.

class ProfileClassView(View):
    def get(self,request,id):
        if 'id' not in request.session:
            return redirect('login')
        result = User.objects.get(pk=id)
        profile_form = ProfileUpdateForm(instance=result)
        return render(request, 'profile_app/profile.html', {'forms': profile_form, 'user': result})

    def post(self,request, id):
        result = User.objects.get(pk=id)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=result)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,"Profile updated successfully!")
            return render(request, 'profile_app/profile.html', {'forms': profile_form,'user': result})
        else:
            return render(request, 'profile_app/profile.html', {'forms': profile_form,'user': result})
