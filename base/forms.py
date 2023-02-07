from django.forms import ModelForm
from .models import Category, Law, Document, Departament, Status
from django import forms
from taggit.forms import TagField


class AuthForm(forms.Form):
    username = forms.CharField(
        label=("Логин"),
        max_length=15,
        widget=forms.TextInput(attrs={
            "autocomplete": "username",
            "class": "form-control",
        }),
    )

    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "class": "form-control",
        }),
    )


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title']


class DepartamentForm(ModelForm):
    class Meta:
        model = Departament
        fields = ['title']


class LawForm(ModelForm):
    class Meta:
        model = Law
        fields = ['shorttitle']


class DocumentForm(ModelForm):

    title = forms.CharField(
        label='Заголовок:',
        max_length=250
    )
    category = forms.ModelChoiceField(
        label='Категория:',
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }))
    departament = forms.ModelChoiceField(
        required=False, label='Отдел:',
        queryset=Departament.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }))
    status = forms.ModelChoiceField(
        required=False, label='Статус:',
        queryset=Status.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }))
    law = forms.ModelMultipleChoiceField(
        required=False, label='Закон:',
        queryset=Law.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-select",
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
    tags = TagField(label='Теги:',
                    required=False,
                    widget=forms.Textarea(
                        attrs={
                            "class": "form-control"
                            }),
                    )

    class Meta:
        model = Document
        fields = ['title', 'category', 'departament',
                  'status', 'law', 'text', 'tags']


class SearchForm(ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'category', 'departament', 'status', 'law', 'text']
