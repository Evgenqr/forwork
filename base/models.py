from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


def category_directory_path(instance, filename):
    return 'category_{0}/{1}'.format(instance.category.title, filename)

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
    slug = models.SlugField("Ссылка", max_length=250, unique=True)

    class Meta:
        verbose_name = "Закон"
        verbose_name_plural = "Законы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("law_detail", kwargs={"slug": self.slug})
    

# class MyModel(models.Model):
#     upload = models.FileField(upload_to=user_directory_path)
    
    
class Document(models.Model):
    title = models.CharField(verbose_name="Документ", max_length=250)
    slug = models.SlugField("Ссылка", max_length=250, unique=True)
    user = models.ForeignKey(User,
                            verbose_name="Пользователь",
                            on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    law = models.ManyToManyField(Law, verbose_name="Закон", related_name="document_law", blank=True, null=True)
    text = models.TextField(verbose_name="Текст", blank=True, null=True)
    file = models.FileField(verbose_name="Вложения", blank=True, null=True, upload_to=category_directory_path)
    date_create = models.DateTimeField(auto_now_add = True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now = True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("document_detail", kwargs={"slug": self.slug})
