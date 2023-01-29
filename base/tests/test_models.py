# from django.test import TestCase
from base.models import Status, Departament, Law, Category, Document
import pytest


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

# class Topping(models.Model):
#     # ...
#     pass
# topping.pizza_set
# class Pizza(models.Model):
#     toppings = models.ManyToManyField(Topping)
# >>> e = b.entry_set.create(
# ...     headline='Hello',
# ...     body_text='Hi',
# ...     pub_date=datetime.date(2005, 1, 1)
# ... )
# https://django.fun/ru/docs/django/4.1/ref/models/relations/


@pytest.mark.django_db
def test_document_creation():
    category = Category.objects.create(title="Судебная практика")
    departament = Departament.objects.create(title="Канцелярия")
    law = Law.objects.create(title="Федеральный закон №59", shorttitle="59-ФЗ")
    status = Status.objects.create(title="Архив")
    document = Document.objects.create(title="Практика закона о торгавли",
                                       category=category,
                                       law=law.set(),
                                       departament=departament,
                                       status=status,
                                       text="Тестовая страница с текстом.",
                                       date_create="29-01-2023"
                                       )
    assert document.title == "Практика закона о торгавли"
    assert document.category == "Судебная практика"
    assert document.law == ("Федеральный закон №59",)
    assert document.departament == "Канцелярия"
    assert document.status == "Архив"
    assert document.text == "естовая страница с текстом."
    assert document.date_create == "29-01-2023"


# class StatusTest(TestCase):

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.status = Status.objects.create(title='Тестовый статус')

#     def test_text_convert_to_slug(self):
#         status = StatusTest.status
#         slug = status.slug
#         self.assertEqual(slug, 'testovyij-status')


# @pytest.mark.django_db
# def test_models_creation():
#     model = Category.objects.create(title="Тестовая закон")
#     status = Status.objects.create(title="Тестовый статус")
#     departament = Departament.objects.create(title="Тестовый отдел")
#     law = Law.objects.create(title="Тестовый закон")
#     assert model.title == "Тестовая закон"
#     assert status.title == "Тестовый статус"
#     assert departament.title == "Тестовый отдел"
#     assert law.title == "Тестовый закон"
