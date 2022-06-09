from .models import User
from django.contrib.auth.hashers import check_password
class EmailAuthBackend(object):
    def authenticate(self, request,username=None,password=None):
        try:
            user = User.objects.get(email_id=username)
            print(check_password(password, user.password))
            if check_password(password, user.password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoestNotExists:
            return None