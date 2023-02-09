# from django.test import TestCase
from base.models import Status, Departament, Law, Category, Document
import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_dapartament_creation():
    departament = Departament.objects.create(title="Канцелярия")
    assert departament.title == "Канцелярия"
    assert len(departament.title) <= 250
    assert departament.slug == "kantselyariya"


@pytest.mark.django_db
def test_status_creation():
    status = Status.objects.create(title="Архив")
    assert status.title == "Архив"
    assert len(status.title) <= 250
    assert status.slug == "arhiv"


@pytest.mark.django_db
def test_law_creation():
    law = Law.objects.create(title="Федеральный закон №59", shorttitle="59-ФЗ")
    assert law.shorttitle == "59-ФЗ"
    assert len(law.title) <= 250
    assert len(law.shorttitle) <= 50
    assert law.slug == "59-fz"


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(title="Судебная практика")
    assert category.title == "Судебная практика"
    assert category.slug == "sudebnaya-praktika"


@pytest.mark.django_db
def test_document_model():
    user = User.objects.create(username='testuser', password='12345')
    category = Category.objects.create(title='Test Category')
    departament = Departament.objects.create(title='Test Departament')
    status = Status.objects.create(title='Test Status')
    law1 = Law.objects.create(id=1,
                              title="Федеральный закон №59",
                              shorttitle="159-ФЗ")
    law2 = Law.objects.create(id=2,
                              title="Федеральный закон №147",
                              shorttitle="147-ФЗ")
    # Создаем документ
    document = Document.objects.create(
        title='Test Document',
        user=user,
        category=category,
        departament=departament,
        status=status,
        text="Test Text"
    )
    document.law.add(law1, law2)
    assert document.user == user
    assert document.category == category
    assert document.status == status
    assert law1, law2 in document.law.all()
    assert document.date_create is not None
    assert document.date_update is not None
