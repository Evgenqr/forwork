from base_drf.serializers import DocumentSerializer, DocumentDetailSerializer
from base.models import Status, Departament, Category
import pytest
from rest_framework import serializers
from .create_document import create_document


@pytest.mark.django_db
def test_document_serializer():
    document = create_document()
    serializer = DocumentSerializer(document)
    assert serializer.data['title'] == 'TestDocument'
    assert serializer.data['category'] == 'TestCategory'
    assert serializer.data['departament'] == 'TestDepartament'
    assert serializer.data['law'] == ['TestLaw', 'TestLaw2']

    assert serializer.fields['title'].required is True
    assert serializer.fields['category'].required is True
    assert serializer.fields['id'].read_only is True

    assert isinstance(
        serializer.fields['category'], serializers.SlugRelatedField)
    assert isinstance(
        serializer.fields['departament'], serializers.SlugRelatedField)
    assert isinstance(
        serializer.fields['status'], serializers.SlugRelatedField)
    assert isinstance(
        serializer.fields['law'], serializers.ManyRelatedField)


@pytest.mark.django_db
def test_document_detail_serializer():
    document = create_document()
    serializer = DocumentDetailSerializer(document)

    assert serializer.fields['title'].read_only is False
    assert serializer.fields['id'].read_only is True

    assert serializer.fields['category'].queryset & Category.objects.all()
    assert serializer.fields['departament'].queryset & Departament.objects.all(
    )
    assert serializer.fields['status'].queryset & Status.objects.all()

    assert serializer.data['title'] == 'TestDocument'
    assert serializer.data['category'] == 'TestCategory'
    assert serializer.data['departament'] == 'TestDepartament'
    assert serializer.data['status'] == 'TestStatus'
    assert serializer.data['law'] == ['TestLaw', 'TestLaw2']
