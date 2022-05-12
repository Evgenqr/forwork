from django.core.exceptions import ValidationError
import os
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.core import validators


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
        return reverse("category_detail", kwargs={"slug": self.slug})


class Law(models.Model):
    title = models.CharField(verbose_name="Закон", max_length=250)
    shorttitle = models.CharField(
        verbose_name="Сокращенное название закона", max_length=50)
    slug = models.SlugField("Ссылка", max_length=250, unique=True)

    class Meta:
        verbose_name = "Закон"
        verbose_name_plural = "Законы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("law_detail", kwargs={"slug": self.slug})


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


class Document(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=250)
    slug = models.SlugField("Ссылка", max_length=250, unique=True)
    user = models.ForeignKey(User,
                             verbose_name="Пользователь",
                             on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, verbose_name="Категория", related_name="categories",
        on_delete=models.CASCADE)
    law = models.ManyToManyField(
        Law, verbose_name="Закон",
        blank=True)
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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("document_detail", kwargs={"slug": self.slug})


def validate_file_type(value):
    accepted_extensions = ['.png', '.jpg', '.jpeg', '.pdf']
    extension = os.path.splitext(value.name)[1]
    if extension not in accepted_extensions:
        raise ValidationError(u'{} is not an accepted file type'.format(value))


class DocumentFile(models.Model):
    document = models.ForeignKey(
        Document, verbose_name="Вложения11", on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Вложения", blank=True,
                            null=True, upload_to=file_directory_path,
                            help_text="Максимальный размер файла: 50 МБ. Разрешённые типы файлов: txt doc docx xls xlsx pdf png jpg rar zip ppt pptx rtf gif.",
                            validators=[validate_file_type])

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
        print('-------', extension)
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
