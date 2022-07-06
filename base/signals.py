from turtle import update
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Document, DocumentFile
from django.db.models import signals

 
@receiver(pre_save, sender=Document)
def post_delete_file(sender, **kwargs):
    pass
    # print('post delete')
    # arr_of_id = request.POST.getlist('arr_of_id[]')
    # print('!!!!', arr_of_id)
    # arr_of_id = request.GET.getlist('arr_of_id[]')
    # print('!!!!', arr_of_id)