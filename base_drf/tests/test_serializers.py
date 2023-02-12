from base_drf.serializers import DocumentSerializer, DocumentDetailSerializer
from base.models import Status, Departament, Law, Category, Document
from django.contrib.auth.models import User
import pytest
from rest_framework import serializers


def create_document():
    user = User.objects.create(username='testuser', password='12345')
    category = Category.objects.create(title='TestCategory')
    departament = Departament.objects.create(title='TestDepartament')
    status = Status.objects.create(title='TestStatus')
    law1 = Law.objects.create(shorttitle='TestLaw')
    law2 = Law.objects.create(shorttitle='TestLaw2')
    document = Document.objects.create(
        user=user,
        title='TestDocument', category=category, departament=departament,
        status=status)
    document.save()
    document.law.add(law1, law2)
    return document


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
