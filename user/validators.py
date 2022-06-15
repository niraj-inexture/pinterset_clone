import re
from django import forms

class PasswordValidator:

    def validate(self, password, user=None):
        expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

        if not re.search(expression,password):
            raise forms.ValidationError('Password must contain minimum one uppercase character, one lowercase character, one digit and one special character.')

    def get_help_text(self):
        return 'Password must contain minimum one uppercase character, one lowercase character, one digit and one special character.'