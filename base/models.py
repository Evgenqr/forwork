from venv import create
from django.core.exceptions import ValidationError
import os
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.core import validators
import uuid



def file_directory_path(instance, filename):
    return 'uploads/{0}/{1}'.format(instance.document.title, filename)


class Category(models.Model):
    title = models.CharField(verbose_name="Категория", max_length=250)
    slug = models.SlugField("Ссылка", max_length=250, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category", kwargs={"slug": self.slug})


class Law(models.Model):
    title = models.CharField(verbose_name="Закон", max_length=250)
    shorttitle = models.CharField(
        verbose_name="Сокращенное название закона", max_length=50)
    slug = models.SlugField("Ссылка", max_length=250, unique=True)

    class Meta:
        verbose_name = "Закон"
        verbose_name_plural = "Законы"

    def __str__(self):
        return self.shorttitle

    def get_absolute_url(self):
        return reverse("law", kwargs={"slug": self.slug})

class Departament(models.Model):
    title = models.CharField(verbose_name="Название отдела", max_length=250)
    slug = models.SlugField("Ссылка", max_length=250, unique=True)

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("departament", kwargs={"slug": self.slug})
    

class Status(models.Model):
    title = models.CharField(verbose_name="Статус", max_length=250)
    slug = models.SlugField("Ссылка", max_length=250, unique=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статус"
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("status", kwargs={"slug": self.slug})

    
class Document(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=250)
    # slug = models.SlugField("Ссылка", max_length=250, unique=True)
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User,
                             verbose_name="Пользователь",
                             on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, verbose_name="Категория", related_name="categories",
        on_delete=models.CASCADE)
    law = models.ManyToManyField(
        Law, verbose_name="Закон",
        blank=True)
    departament = models.ForeignKey(
        Departament, verbose_name="Отдел", related_name="departaments",
        blank=True, null=True,
        on_delete=models.CASCADE)
    status = models.ForeignKey(
        Status, verbose_name="Статус", related_name="status",
        blank=True, null=True,
        on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст", blank=True, null=True)
    # file = models.FileField(verbose_name="Вложения", blank=True,
    #                         null=True, upload_to=file_directory_path)
    date_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("document_detail", kwargs={"slug": self.slug})

    def validate_file_type(value):
        FILE_EXT_WHITELIST = ['.pdf', '.txt', '.doc', '.docx', '.rtf',
                            '.xls', '.xlsx', '.ppt', '.pptx', '.png',
                            '.bmp', '.jpg', '.gif', '.zip', '.rar']
        extension = os.path.splitext(value.name)[1]
        if extension not in FILE_EXT_WHITELIST:
            raise ValidationError(u'{} is not an accepted file type'.format(value))


class DocumentFile(models.Model):
    document = models.ForeignKey(
        Document, verbose_name="Документ", blank=True,
                            null=True, on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Вложения", blank=True,
                            null=True, upload_to=file_directory_path)

    class Meta:
        verbose_name = "Приложение"
        verbose_name_plural = "Приложения"

    def __str__(self):
        return self.document.title

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def css_class(self):
        extension = os.path.splitext(self.file.name)[1]
        # print('-------', extension)
        if extension == '.pdf':
            return 'pdf'
        if extension == '.doc' or extension == '.docx' or extension == '.rtf':
            return 'word'
        if extension == '.xls' or extension == '.xlsx':
            return 'excel'
        if extension == '.ppt' or extension == '.pptx':
            return 'powpoint'
        if extension == '.png' or extension == '.jpg' or extension == '.gif':
            return 'fileimg'
        if extension == '.zip' or extension == '.rar':
            return 'archive'
        if extension == '.txt':
            return 'textfile'
        return 'other'


# from django.db.models import signals
# from django.shortcuts import get_object_or_404 

# def pre_test(sender, instance, *args, **kwargs):
#     if create:
#         print('dd')
#     else:
#         print('ne')
#     file = get_object_or_404(DocumentFile, pk=instance.pk)
#     slug = file.document.slug
#     document = get_object_or_404(Document, slug=slug)
#     files = DocumentFile.objects.filter(document=document)
#     for f in files:
#         print ("Pre", f.filename)
#     # print(args, kwargs)

# signals.pre_save.connect(receiver=pre_test, sender=DocumentFile)


# def post_test(sender, instance, *args, **kwargs):
#     if create:
#         print('dd2')
#     else:
#         print('ne2')
    
    # file = get_object_or_404(DocumentFile, pk=instance.pk)
    # slug = file.document.slug
    # document = get_object_or_404(Document, slug=slug)
    # files = DocumentFile.objects.filter(document=document)
    # for f in files:
    #     print ("Pre", f.filename, f.pk)

# signals.post_save.connect(receiver=post_test, sender=DocumentFile)





# class Document(models.Model):
#     title = models.CharField(verbose_name="Заголовок", max_length=250)
#     slug = models.SlugField("Ссылка", max_length=250, unique=True)
#     user = models.ForeignKey(User,
#                              verbose_name="Пользователь",
#                              on_delete=models.CASCADE)
#     category = models.ForeignKey(Category,
#                                  verbose_name="Категория",
#                                  on_delete=models.CASCADE)
#     law = models.ManyToManyField(Law,
#                                  verbose_name="Закон",
#                                  related_name="document_law", blank=True)
#     text = models.TextField(verbose_name="Текст", blank=True, null=True)
#     date_create = models.DateTimeField(auto_now_add=True,
#                                        verbose_name="Дата создания")
#     date_update = models.DateTimeField(auto_now=True,
#                                        verbose_name="Дата обновления")
#     file = models.ForeignKey(File, verbose_name="Файл", blank=True,
#                              null=True,
#                              on_delete=models.CASCADE)
    # file = models.FileField(verbose_name="Вложения", blank=True,
    #                         null=True, upload_to=category_directory_path)
    # file_name = models.CharField(verbose_name="Заголовок", max_length=250)
    # category = models.ForeignKey(Category,
    #                              verbose_name="Категория",
    #                              on_delete=models.CASCADE)

    # def filename(self):
    #     return os.path.basename(self.file.name)

    # class Meta:
    #     verbose_name = "Документ"
    #     verbose_name_plural = "Документы"

    # def __str__(self):
    #     return self.title

    # def get_absolute_url(self):
    #     return reverse("document_detail", kwargs={"slug": self.slug})



# class File(models.Model):
#     title = models.CharField(verbose_name="Название файла", max_length=100,
#                              blank=True, null=True)
#     file = models.FileField(verbose_name="Вложения", blank=True,
#                             null=True, max_length=200,
#                             upload_to=file_directory_path,
#                             validators=[validate_image_file_extension])
#     # validators=[FileExtensionValidator(
#     #     allowed_extensions=['pdf'])])

#     def filename(self):
#         return os.path.basename(self.file.name)

#     class Meta:
#         verbose_name = "Вложение"
#         verbose_name_plural = "Вложения"

#     def __str__(self):
#         return self.title
