from turtle import update
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Document, DocumentFile
from django.db.models import signals

 
@receiver(post_delete, sender=DocumentFile)
def post_delete_file(sender, **kwargs):
    print('post delete')