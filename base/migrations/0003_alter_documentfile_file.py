# Generated by Django 3.2.9 on 2022-05-11 18:18

import base.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_documentfile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfile',
            name='file',
            field=models.FileField(blank=True, help_text='Максимальный размер файла: 500 МБ. Разрешённые типы файлов: txt doc docx xls xlsx pdf png jpg rar zip ppt pptx rtf gif.', null=True, upload_to=base.models.file_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name='Вложения'),
        ),
    ]
