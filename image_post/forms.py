from django import forms
from image_post.models import ImageStore, ImageSave
from topic.models import Topic


class UploadImageForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = ImageStore
        fields = ['topic', 'user', 'image_type', 'image_path', 'description']
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'image_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_image_path(self):
        img = self.cleaned_data['image_path']
        img_type = img.name.split('.')
        type_list = ['BMP', 'JPEG', 'PNG', 'TIFF', 'WEBP', 'JPG']
        if img_type[-1].upper() not in type_list:
            raise forms.ValidationError('Image can upload in bmp, jpeg, png, tiff or webp format.')
        return img


class ImageSaveForm(forms.ModelForm):
    class Meta:
        model = ImageSave
        fields = ['user', 'image_path', 'is_save']
        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'image_path': forms.HiddenInput(attrs={'class': 'form-control'}),
            'is_save': forms.HiddenInput(attrs={'class': 'form-control'}),
        }


class UpdateImageDescriptionForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = ImageStore
        fields = ['topic', 'image_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
