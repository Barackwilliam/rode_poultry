from .models import GalleryMedia
from django import forms


class GalleryMediaAdminForm(forms.ModelForm):
    class Meta:
        model = GalleryMedia
        fields = '__all__'

    class Media:
        js = [
            'https://ucarecdn.com/libs/widget/3.x/uploadcare.full.min.js',
        ]