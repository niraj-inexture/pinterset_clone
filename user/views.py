from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import ModelFormRegistration, ModelFormLogin, ProfileUpdateForm, PasswordChangeCustomForm
from .authentication import EmailAuthBackend
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from image_post.models import ImageStore


# Create your views here.

class HomeClassView(View):
    def get(self, request):
        if request.user.is_authenticated:
            get_image = ImageStore.objects.filter(approve_status=True, image_type='Public')
            return render(request, 'user/home.html', {'images': get_image})
        else:
            return redirect('index')


# This class view is used to render index page
class IndexClassView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'user/index.html')


# This class view is used to render register page and register user
class RegisterClassView(View):
    def get(self, request):
        register = ModelFormRegistration()
        return render(request, 'user/registration.html', {'forms': register})

    def post(self, request):
        register = ModelFormRegistration(request.POST, request.FILES)
        if register.is_valid():
            register.save()
            return redirect('login')
        else:
            return render(request, 'user/registration.html', {'forms': register})


# This view class is used to render login page and login user
class LoginClassView(View):
    def get(self, request):
        login = ModelFormLogin()
        return render(request, 'user/login.html', {"forms": login})

    def post(self, request):
        login_user = ModelFormLogin(request.POST)
        if login_user.is_valid():
            email = login_user.cleaned_data.get('email')
            password = login_user.cleaned_data.get('password')
            user = EmailAuthBackend.authenticate(self, request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email id or password is wrong!')
                return render(request, 'user/login.html', {'forms': login_user})
        else:
            return render(request, 'user/login.html', {'forms': login_user})


# This class view is used to logout user
class LogoutClassView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('index')
        else:
            return redirect('index')


# This class view is used user profile page load and update
class ProfileClassView(View):
    def get(self, request):
        if request.user.is_authenticated:
            profile_form = ProfileUpdateForm(instance=request.user)
            return render(request, 'user/profile.html', {'forms': profile_form})
        else:
            return redirect('index')

    def post(self, request):
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            return render(request, 'user/profile.html', {'forms': profile_form})


# This class view is used for change password
class ChangePasswordView(View):
    def get(self, request):
        if request.user.is_authenticated:
            change_pass = PasswordChangeCustomForm(user=request.user)
            return render(request, 'user/change_password.html', {'forms': change_pass})
        else:
            return redirect('index')

    def post(self, request):
        if request.user.is_authenticated:
            change_pass = PasswordChangeCustomForm(user=request.user, data=request.POST)
            if change_pass.is_valid():
                change_pass.save()
                update_session_auth_hash(request, change_pass.user)
                messages.success(request, "Password updated successfully!")
                return redirect('change-password')
            else:
                return render(request, 'user/change_password.html', {'forms': change_pass})
        else:
            return redirect('index')
