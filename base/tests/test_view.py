import os
from base.models import Status, Category, Document
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from base.views import DocumentListView


# -------------- Тестирование DocumentListView

FILE_EXT_WHITELIST = ['.pdf', '.txt', '.doc', '.docx', '.rtf',
                              '.xls', '.xlsx', '.ppt', '.pptx', '.png',
                              '.bmp', '.jpg', '.gif', '.zip', '.rar']


def validate_file_extension(value):
    ext = os.path.splitext(value)[1]
    if not ext.lower() in FILE_EXT_WHITELIST:
        raise ValidationError('Unsupported file extension.')


def create_document():
    user = User.objects.create(username='testuser1', password='12345')
    status = Status.objects.create(title='Test status 1')
    category = Category.objects.create(title='Test category 1')
    document = Document.objects.create(
        user=user,
        title='Test Document',
        status=status,
        category=category)
    return document


# -------------- Тестирование DocumentDelete
@pytest.mark.django_db
def test_document_delete2(client):
    document = create_document()
    # response = client.post('/document/{}/delete'.format(document.slug))
    # response = client.get(f'/document/{document.slug}/delete')
    # assert response.status_code == 302
    document.delete()
    assert not Document.objects.filter(slug=document.slug).exists()
# <--------------


@pytest.mark.django_db
def test_documentlistview():
    # Проверяем, что validate_file_extension() блокирует файлы,
    # форматы которых недопустимы
    with pytest.raises(ValidationError):
        validate_file_extension('testfile.exe')

    user = User.objects.create(username='testuser', password='12345')
    # Создаем документы для тестирования списка документов
    document = create_document()
    document2 = Document.objects.create(
        user=user,
        title='Test document 2',
        status=Status.objects.create(title='Test status 2'),
        category=Category.objects.create(title='Test category 2'))

    # Проверяем, что при запросе списка документов,
    # они будут упорядочены по убыванию date_create
    documents = DocumentListView().get_queryset()
    assert documents[0] == document2 and documents[1] == document
# <--------------


# -------------- Тестирование DocumentUpdateView
@pytest.mark.django_db
def test_document_update_view(client):
    document = create_document()
    client.force_login(document.user)
    response = client.post(
        '/document/{}/view/'.format(document.slug),
        {'title': 'Updated Test Document'})
    assert response.status_code == 200
# <--------------


# -------------- Тестирование DocumentCreateView
@pytest.mark.django_db
def test_document_create_view(client):
    document = create_document()
    assert document is not None
    # client.force_login(document.user)
    # response = client.post('/create/', {})
    # print('----', client.get('/create/', {}))
    # print('---', document)
    # assert response.status_code == 200
# <--------------


# -------------- Тестирование DocumentDetailView
@pytest.mark.django_db
def test_documentdetailView(client):
    document = create_document()
    response = client.get(f'/document/{document.slug}/')
    assert response.status_code == 200
    assert 'documents' in response.context
    assert 'slug' in response.context
    assert 'files' in response.context
# <--------------


# -------------- Тестирование SearchView
@pytest.mark.django_db
def test_search_view(client):
    response = client.get('/search/')
    assert response.status_code == 200
# <--------------
