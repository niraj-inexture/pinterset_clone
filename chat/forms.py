from django import forms
from django.db.models import Q
from .models import Thread

class ThreadForm(forms.ModelForm):
    def clean(self):
        super(ThreadForm,self).clean()
        first_person = self.cleaned_data.get('first_person')
        second_person = self.cleaned_data.get('second_person')

        lookup1 = Q(first_person=first_person) | Q(second_person=first_person)
        lookup2 = Q(first_person=second_person) | Q(second_person=second_person)
        lookup = Q(lookup1 | lookup2)

        qs = Thread.objects.filter(lookup)
        if qs.exists():
            pass