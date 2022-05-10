import os
from statistics import mode
# from pydoc import Doc
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# from django.core import validators


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


class File(models.Model):
    title = models.CharField(verbose_name="Название файла", max_length=100,
                             blank=True, null=True)
    file = models.FileField(verbose_name="Вложения", blank=True,
                            null=True, max_length=200,
                            upload_to=file_directory_path)

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"

    def __str__(self):
        return self.title


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


class DocumentFile(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    file = models.FileField(verbose_name="Вложения", blank=True,
                            null=True, upload_to=file_directory_path)

    def __str__(self):
        return self.document.title

    @property
    def filename(self):
        return os.path.basename(self.file.name)

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
