from django.forms import ModelForm
from .models import Category, Law, Document
from django import forms


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title']


class LawForm(ModelForm):
    class Meta:
        model = Law
        fields = ['shorttitle']


# class FileForm(ModelForm):
#     class Meta:
#         model = File
#         fields = ['title', 'file']


class DocumentForm(ModelForm):
    files = forms.FileField(required=False, widget=forms.FileInput(
        attrs={
            "class": "form-control",
            "multiple": True
        }))

    class Meta:
        model = Document
        fields = ['title', 'category', 'law', 'text']
