from csv import list_dialects
from django.contrib import admin
from .models import Category, Law, Document, DocumentFile, Departament

# admin.site.register(Document)
# admin.site.register(Law)
# admin.site.register(Category)
# admin.site.register(DocumentFile)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'user', 'departament', 'category', 'date_create']
    prepopulated_fields = {'slug': ('title',), }


@admin.register(Law)
class LawAdmin(admin.ModelAdmin):
    list_display = ['title', 'shorttitle', 'slug']
    prepopulated_fields = {'slug': ('shorttitle',), }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',), }
    
@admin.register(Departament)
class Departament(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',), }
    
@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    list_display = ['document', 'file', 'id', 'document_id']
