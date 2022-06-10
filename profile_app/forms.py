from django import forms
from registration.models import User

GENDER_CHOICES = [
    ("Male",'Male'),
    ('Female','Female'),
    ('Other','Other')
]

class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = User
        fields = ['username','firstname','lastname','email_id','country','gender','profile_image']
        widgets = {
                   'username':forms.TextInput(attrs={'class':'form-control'}),
                   'firstname': forms.TextInput(attrs={'class': 'form-control'}),
                   'lastname': forms.TextInput(attrs={'class': 'form-control'}),
                   'email_id': forms.EmailInput(attrs={'class': 'form-control'}),
                    'country' : forms.Select(attrs={'class': 'form-select'}),
                   'gender':forms.RadioSelect(attrs={'class':'form-check-input'})
                   }

    def clean_username(self):
        uname = self.cleaned_data['username']
        result = User.objects.exclude(pk=self.instance.pk).filter(username=uname).exists()
        if result:
            raise forms.ValidationError('Username already exists')
        return uname

    def clean_email_id(self):
        uemail = self.cleaned_data['email_id']
        result = User.objects.exclude(pk=self.instance.pk).filter(email_id=uemail).exists()
        if result:
            raise forms.ValidationError('Email id already exists')
        return uemail

    def clean_firstname(self):
        fname = self.cleaned_data['firstname']
        if not fname.isalpha():
            raise forms.ValidationError('Firstname only contain alphabet')
        return fname

    def clean_lastname(self):
        lname = self.cleaned_data['lastname']
        if not lname.isalpha():
            raise forms.ValidationError('Firstname only contain alphabet')
        return lname
