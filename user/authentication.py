from .models import RegisterUser
from django.contrib.auth.hashers import check_password

class EmailAuthBackend(object):
    def authenticate(self, request,username=None,password=None):
        try:
            user = RegisterUser.objects.get(email=username)
            if check_password(password, user.password):
                return user
            return None
        except RegisterUser.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            return RegisterUser.objects.get(pk=user_id)
        except RegisterUser.DoesNotExist:
            return None