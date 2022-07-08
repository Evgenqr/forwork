from turtle import update
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Document, DocumentFile
from .forms import DocumentForm
from django.db.models import signals
from django.shortcuts import redirect, render, get_object_or_404

 
# @receiver(pre_save, sender=Document)
# def delete_file(request, pk, **kwargs):
#     file = get_object_or_404(DocumentFile, pk=pk)
#     slug = file.document.slug
#     document = get_object_or_404(Document, slug=slug)
#     print('dellll')
#     file.delete()
#     form = DocumentForm(instance=document)
#     files = DocumentFile.objects.filter(document=document)
#     return render(request, 'base/viewdocument.html', {
#             'document': document,
#             'files': files,
#             'form': form
#         })
    
    
#     document = get_object_or_404(Document, slug=slug)
    # print('post delete')
    # arr_of_id = request.POST.get('arr_of_id[]')
    # print('!!!!', arr_of_id)
    # arr_of_id = request.GET.getlist('arr_of_id[]')
    # print('!!!!', arr_of_id)
    
# @login_required
# def deletefile(request, pk):
#     file = get_object_or_404(DocumentFile, pk=pk)
#     slug = file.document.slug
#     document = get_object_or_404(Document, slug=slug)
#     if request.method == 'GET':
#         file.delete()
#         form = DocumentForm(instance=document)
#         files = DocumentFile.objects.filter(document=document)
#         return render(request, 'base/viewdocument.html', {
#             'document': document,
#             'files': files,
#             'form': form
#         })