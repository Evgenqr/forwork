from django.contrib import admin
from .models import Category, Law, Document, File

admin.site.register(Document)
admin.site.register(Law)
admin.site.register(Category)
admin.site.register(File)
