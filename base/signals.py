# from turtle import update
# from django.db.models.signals import post_save, pre_save, post_delete
# from django.dispatch import receiver
# from .models import Document, DocumentFile
# from .forms import DocumentForm
# from django.db.models import signals
# from django.shortcuts import redirect, render, get_object_or_404


# @receiver(pre_save, sender=Document)
# def delete_file(request, **kwargs):
#     if request.is_ajax():
#         arr_of_id = request.POST.getlist("arr_of_id[]")
#         for f_id in arr_of_id:
#             file = get_object_or_404(DocumentFile, pk=f_id)
#             slug = file.document.slug
#             document = get_object_or_404(Document, slug=slug)
#             file.delete()
