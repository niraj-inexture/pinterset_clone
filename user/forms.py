from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from topic.models import Topic
from .models import RegisterUser, Boards

GENDER_CHOICES = [
    ("Male", 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
]


class ModelFormRegistration(UserCreationForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = RegisterUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'country', 'gender',
                  'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(ModelFormRegistration, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        uemail = self.cleaned_data['email']
        result = RegisterUser.objects.exclude(pk=self.instance.pk).filter(email=uemail).exists()
        if result:
            raise forms.ValidationError('Email id already exists')
        return uemail

    def clean_first_name(self):
        """This method is used to validate firstname"""

        fname = self.cleaned_data['first_name']
        if not fname.isalpha():
            raise forms.ValidationError('Firstname only contain alphabet')
        return fname

    def clean_last_name(self):
        """This method is used to validate lastname"""

        lname = self.cleaned_data['last_name']
        if not lname.isalpha():
            raise forms.ValidationError('Firstname only contain alphabet')
        return lname


class ModelFormLogin(forms.ModelForm):
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = RegisterUser
        fields = ['email', 'password']
        widgets = {'password': forms.PasswordInput(attrs={'class': 'form-control'}),
                   }


class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = RegisterUser
        fields = ['username', 'first_name', 'last_name', 'email', 'country', 'gender', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.RadioSelect(attrs={'class': 'form-check-input'})
        }

    def clean_email(self):
        uemail = self.cleaned_data['email']
        result = RegisterUser.objects.exclude(pk=self.instance.pk).filter(email=uemail).exists()
        if result:
            raise forms.ValidationError('Email id already exists')
        return uemail

    def clean_first_name(self):
        fname = self.cleaned_data['first_name']
        if not fname.isalpha():
            raise forms.ValidationError('Firstname only contain alphabet')
        return fname

    def clean_last_name(self):
        lname = self.cleaned_data['last_name']
        if not lname.isalpha():
            raise forms.ValidationError('Firstname only contain alphabet')
        return lname


class PasswordChangeCustomForm(PasswordChangeForm):

    def __init__(self, user, *args, **kwargs):
        super(PasswordChangeCustomForm, self).__init__(user, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ModelFormActivateAccount(forms.ModelForm):
    class Meta:
        model = RegisterUser
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CreateBoardForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all().order_by('-total_likes'),
                                   widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Boards
        fields = ['topic', 'user']
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
        }