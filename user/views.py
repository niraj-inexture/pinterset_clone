from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from topic.models import Topic
from .forms import ModelFormRegistration, ModelFormLogin, ProfileUpdateForm, PasswordChangeCustomForm, \
    ModelFormActivateAccount, CreateBoardForm
from .authentication import EmailAuthBackend
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from image_post.models import ImageStore, BoardImages
from .models import RegisterUser, Boards

# Create your views here.
from .token import account_activation_token


class HomeClassView(View):
    """
       show all images uploaded by user

       **Context**

       ``images``
           An instance of :model:`image_post.ImageStore`.

       **Template:**

           :template:`user/home.html`

    """

    def get(self, request):
        if request.user.is_authenticated:
            get_image = ImageStore.objects.filter(approve_status=True, image_type='Public')
            return render(request, 'user/home.html', {'images': get_image})
        else:
            return redirect('index')


class IndexClassView(View):
    """
       show index page

       **Context**

            No context

       **Template:**

           :template:`user/index.html`

        """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'user/index.html')


class RegisterClassView(View):
    """
       register user :model:`user.RegisterUser`.

       **Context**

       ``forms``
           Registration form

       **Template:**

           :template:`user/registration.html`

    """

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


class LoginClassView(View):
    """
       login user :model:`user.RegisterUser`.

       **Context**

       ``forms``
           Login form

       **Template:**

           :template:`user/login.html`

    """

    def get(self, request):
        login = ModelFormLogin()
        return render(request, 'user/login.html', {"forms": login})

    def post(self, request):
        login_user = ModelFormLogin(request.POST)
        if login_user.is_valid():
            email = login_user.cleaned_data.get('email')
            password = login_user.cleaned_data.get('password')
            emailauth = EmailAuthBackend()
            user = emailauth.authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Your account is not active!Please first activate your account.')
                    return render(request, 'user/login.html', {'forms': login_user})
            else:
                messages.error(request, 'Email id or password is wrong!')
                return render(request, 'user/login.html', {'forms': login_user})
        else:
            return render(request, 'user/login.html', {'forms': login_user})


class ProfileClassView(View):
    """
       update profile :model:`user.RegisterUser`.

       **Context**

       ``forms``
           Profile update form

       **Template:**

           :template:`user/profile.html`

    """

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


class ChangePasswordView(View):
    """
       change password :model:`user.RegisterUser`.

       **Context**

       ``forms``
           change password form

       **Template:**

           :template:`user/change_password.html`
    """

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


class DeleteAccountClassView(View):
    """
       delete user account :model:`user.RegisterUser`.

       **Context**
            No context

       **Template:**

           No template
    """

    def get(self, request, id):
        user_data = RegisterUser.objects.get(pk=id)
        user_data.delete()
        return redirect('index')


class TopicListClassView(View):
    """
       Get all topics for search :model:`topic.Topic`.

       **Context**

            No context

       **Template:**

           No template
    """

    def get(self, request):
        topics = Topic.objects.all().values_list('topic_name', flat=True)
        topic_list = list(topics)
        return JsonResponse(topic_list, safe=False)


class SearchClassView(View):
    """
       Search images using topic :model:`image_post.ImageStore`.

       **Context**

        ``images``
           An instance of :model:`image_post.ImageStore`.

       **Template:**

           :template:`user/search_topic.html`
    """

    def get(self, request):
        return redirect('home')

    def post(self, request):
        search = request.POST['search']
        topic_id = Topic.objects.get(topic_name=search)
        images = ImageStore.objects.filter(topic=topic_id.id)
        return render(request, 'user/search_topic.html', {'images': images})


class DeactivateUserAccountClassView(View):
    """
       Deactivate account :model:`user.RegisterUser`.

       **Context**

           No context

       **Template:**

           No template
    """

    def get(self, request, id):
        user = RegisterUser.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect('login')


class ActivateUserAccountClassView(View):
    """
       Show activate form and send email to user for activate account.

       **Context**

        ``activation_form``
           User activation form

       **Template:**

            :template:`user/activate_account.html`
            :template:`user/acc_active_email.html'
    """

    def get(self, request):
        activation_form = ModelFormActivateAccount()
        return render(request, 'user/activate_account.html', {'activation_form': activation_form})

    def post(self, request):
        form = ModelFormActivateAccount(request.POST)
        if form.is_valid():
            email = request.POST['email']
            try:
                user = RegisterUser.objects.get(email=email)
            except RegisterUser.DoesNotExist:
                user = None
            if user is not None:
                if not user.is_active:
                    current_site = get_current_site(request)
                    mail_subject = 'Activation link has been sent to your email id'
                    message = render_to_string('user/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    email = EmailMessage(
                        subject=mail_subject, body=message, from_email=settings.EMAIL_HOST_USER, to=[email]
                    )
                    email.send()
                    messages.success(request, 'email successfully send to your email id.')
                else:
                    messages.error(request, 'You are already activate!')
            else:
                messages.error(request, 'Email id is not valid!')
        return render(request, 'user/activate_account.html', {'activation_form': form})


class ActivateAccountClassView(View):
    """
       Activate account.

       **Context**

            No context

       **Template:**

            :template:`user/activate_success.html`
    """

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = RegisterUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, RegisterUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        else:
            messages.error(request, 'Activation link is invalid!')
        return render(request, 'user/activate_success.html')


class CreateBoardClassView(View):
    """
       show board form and create boards.

       **Context**

        ``board``
          Board form

        ``boards_name``
          An instance of :model:`user.Boards`.

       **Template:**

            :template:`user/create_board.html`
    """

    def get(self, request):
        board = CreateBoardForm(initial={'user': request.user.id})
        boards_obj = Boards.objects.filter(user=request.user.id)
        return render(request, 'user/create_board.html', {'board': board, 'boards_name': boards_obj})

    def post(self, request):
        topic_id = request.POST.get('topic_id')
        board_obj_verify = Boards.objects.filter(user=request.user.id, topic=topic_id)
        if board_obj_verify:
            message = messages.error(request, 'Board already created')
            return JsonResponse({'status': 1, 'message': message})
        else:
            topic_obj = Topic.objects.get(id=topic_id)
            board = Boards(user=request.user, topic=topic_obj)
            board.save()
            message = messages.success(request, 'Board created successfully')
            return JsonResponse({'status': 1, 'message': message})


class ShowImagesInBoardClassView(View):
    """
       Show board images :model:`image_post.BoardImages`.

       **Context**

        ``boards_images``
           An instance of :model:`image_post.BoardImages`.

       **Template:**

            :template:`user/board_images.html`
    """

    def get(self, request, pk):
        boards_image_obj = BoardImages.objects.filter(user=request.user.id, topic=pk)
        return render(request, 'user/board_images.html', {'boards_images': boards_image_obj})


class DeleteBoardImageClassView(View):
    """
       Delete one image from board :model:`image_post.BoardImages`.

       **Context**

            No Context

       **Template:**

            No template
    """

    def post(self, request):
        if request.user.is_authenticated:
            id = request.POST.get('sid')
            boardimage_obj = BoardImages.objects.get(user=request.user.id, image_post=id)
            boardimage_obj.delete()
            return JsonResponse({'status': 1})
        else:
            return redirect('index')


class DeleteBoardClassView(View):
    """
       Delete particular one board :model:`user.Boards`.

       **Context**

            No Context

       **Template:**

            No template
    """

    def post(self, request):
        if request.user.is_authenticated:
            id = request.POST.get('topic_id')
            boards_obj = Boards.objects.get(user=request.user.id, topic=id)
            boards_obj.delete()
            BoardImages.objects.filter(user=request.user.id, topic=id).delete()
            return JsonResponse({'status': 1})
        else:
            return redirect('index')