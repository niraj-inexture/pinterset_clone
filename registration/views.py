from django.shortcuts import render, redirect
from .forms import ModelFormRegistration, ModelFormLogin
from django.views import View
from .models import User
from django.contrib.auth.hashers import make_password
from .authentication import EmailAuthBackend
from django.contrib import messages

# Create your views here.
class IndexClassView(View):
    def get(self, request):
        return render(request, 'index.html')

class RegisterClassView(View):
    def get(self, request):
        if 'id' in request.session:
            return redirect('home')
        register = ModelFormRegistration()
        return render(request, 'registration/registration.html', {'forms': register})

    def post(self, request):
        register = ModelFormRegistration(request.POST, request.FILES)
        if register.is_valid():
            username = register.cleaned_data.get('username')
            firstname = register.cleaned_data.get('firstname')
            lastname = register.cleaned_data.get('lastname')
            email_id = register.cleaned_data.get('email_id')
            password = register.cleaned_data.get('password')
            country = register.cleaned_data.get('country')
            gender = register.cleaned_data.get('gender')
            profile_image = register.cleaned_data.get('profile_image')
            hash_password = make_password(password)
            register = User(username=username,
                            firstname=firstname,
                            lastname=lastname,
                            email_id=email_id,
                            password=hash_password,
                            country=country,
                            gender=gender,
                            profile_image=profile_image
                            )
            register.save()
            return redirect('login')
        else:
            return render(request, 'registration/registration.html', {'forms': register})

class LoginClassView(View):
    def get(self, request):
        if 'id' in request.session:
            return redirect('home')
        login = ModelFormLogin()
        return render(request, 'registration/login.html', {"forms": login})

    def post(self, request):
        login_user = ModelFormLogin(request.POST)
        if login_user.is_valid():
            email = login_user.cleaned_data.get('email_id')
            password = login_user.cleaned_data.get('password')
            user = EmailAuthBackend.authenticate(self, request, username=email, password=password)
            if user is not None:
                request.session['id'] = user.id
                return redirect('home')
            else:
                messages.error(request,'Email id or password is wrong!')
                return render(request, 'registration/login.html', {'forms': login_user})
        else:
            return render(request, 'registration/login.html', {'forms': login_user})

class LogoutClassView(View):
    def get(self, request):
        if 'id' in request.session:
            request.session.flush()
        return redirect('login')
