from .models import User
def get_user_by_email_and_password(email):
    email = User.objects.get(email_id=email)
    return email

