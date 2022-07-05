from django import forms


class PasswordValidator:

    def validate(self, password, user=None):
        special_char = ['@', '$', '!', '?', '&', '#', '*']

        if not any(chr.isupper() for chr in password):
            raise forms.ValidationError(
                'Password must contain minimum one uppercase character.')

        if not any(chr.islower() for chr in password):
            raise forms.ValidationError(
                'Password must contain minimum one lowercase character.')

        if not any(chr.isdigit() for chr in password):
            raise forms.ValidationError(
                'Password must contain minimum one digit.')

        if not any(chr in special_char for chr in password):
            raise forms.ValidationError(
                'Password must contain minimum one special character.')

    def get_help_text(self):
        return 'Password must contain minimum one uppercase character, one lowercase character, one digit and one ' \
               'special character. '
