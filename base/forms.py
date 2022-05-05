from django.forms import ModelForm
from .models import Category, Law, Document, File
from django import forms


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title']


class LawForm(ModelForm):
    class Meta:
        model = Law
        fields = ['shorttitle']


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ['title', 'file']


class DocumentForm(ModelForm):
    # file = MultiFileField(min_num=1, max_num=7, max_file_size=1024*1024*5,
    #                       label=Document._meta.get_field_by_name(
    #                            'file')[0].verbose_name)
    # files = MultiFileField(min_num=0, max_num=5, max_file_size=1024*1024*5)

    class Meta:
        model = Document
        file = forms.FileField(
            widget=forms.ClearableFileInput(attrs={'multiple': True}))
        fields = ['title', 'category', 'law', 'text', 'file']

        # def save(self, commit=True):
        #     instance = super(DocumentForm, self).save(commit=False)
        #     for each in self.cleaned_data['file']:
        #         File.objects.create(file=each, document=instance)
        #     return instance

# class DocumentForm(ModelForm):
#     attachments = MultiFileField(
    # min_num=1, max_num=3, max_file_size=1024*1024*5)

#     class Meta:
#         model = Document
#         # fields = '__all__'
#         fields = ['title', 'category', 'law', 'text']

#     def save(self, commit=True):
#         instance = super(DocumentForm, self).save(commit=False)
#         for each in self.cleaned_data['attachments']:
#             DocumentFiles.objects.create(file=each, document=instance)
#         return instance
