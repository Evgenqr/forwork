from django.forms import ModelForm
from .models import Category, Law, Document


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title']
    

class LawForm(ModelForm):
    class Meta:
        model = Law
        fields = ['title']
        
        
class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['title']