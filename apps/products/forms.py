from .models import Category,Product
from django import forms



class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    class Media:
        js = [
            'https://ucarecdn.com/libs/widget/3.x/uploadcare.full.min.js',
        ]




class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    class Media:
        js = [
            'https://ucarecdn.com/libs/widget/3.x/uploadcare.full.min.js',
        ]
