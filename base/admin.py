from csv import list_dialects
from django.contrib import admin
from .models import Category, Law, Document, File

# admin.site.register(Document)
admin.site.register(Law)
admin.site.register(Category)
admin.site.register(File)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'user', 'category']
    prepopulated_fields = {'slug': ('title',), }
