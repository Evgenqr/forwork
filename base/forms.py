from tkinter.tix import Select
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

    title = forms.CharField(
        label='Заголовок:',
        max_length=250
        )
    category = forms.ModelChoiceField(
        label='Категория',
        # choices=[(cat.id, cat.title) for cat in Category.objects.all()],
        queryset= Category.objects.all(),
        widget=forms.Select(
            attrs={
                "class":"form-select "
            }))
    law = forms.ModelMultipleChoiceField(
        required=False, label='Закон',
        # choices=[(l.pk, l.shorttitle) for l in Law.objects.all()],
        queryset= Law.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class":"form-select",
            }))
    text = forms.CharField(
        required=False,
        label='Текст:',
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                }),
                           )
    files = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "multiple": True
            }))
    
    class Meta:
        model = Document
        fields = ['title', 'category', 'law', 'text']