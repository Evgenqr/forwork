import pytest
from rest_framework.test import APIClient
from base.models import Document
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated,
)
from base_drf.permissions import IsAdminOrReadOnly
from base_drf.views import (
    DocumentAPIList, DocumentAPIDestroy, DocumentDetailView
)
from base_drf.serializers import DocumentSerializer, DocumentDetailSerializer
# from .test_serializers import create_document
from .create_document import create_document


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_document_api_list(api_client):
    create_document()
    response = api_client.get('/api/v1/documents/')
    view = DocumentAPIList()
    assert response.status_code == 200
    assert view.queryset & Document.objects.all()
    assert view.serializer_class == DocumentSerializer
    assert view.permission_classes == (IsAuthenticatedOrReadOnly, )
    assert response


@pytest.mark.django_db
def test_document_api_destroy(api_client):
    document = create_document()
    view = DocumentAPIDestroy()
    assert view.queryset & Document.objects.all()
    api_client.force_authenticate(user=document.user)
    response = api_client.delete('/api/v1/documents/{}/'.format(document.id))
    assert response.status_code == 204
    assert view.serializer_class == DocumentSerializer
    assert view.permission_classes == (IsAdminOrReadOnly, )
    assert response


@pytest.mark.django_db
def test_document_detail_view(api_client):
    document = create_document()
    api_client.force_authenticate(user=document.user)
    response = api_client.get('/api/v1/documents/{}/'.format(document.id))
    view = DocumentDetailView()
    assert response.status_code == 200
    assert view.queryset & Document.objects.all()
    assert view.serializer_class == DocumentDetailSerializer
    assert view.permission_classes == (IsAuthenticated, )
    assert response
