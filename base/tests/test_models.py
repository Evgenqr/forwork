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

# class Author(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name


# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     authors = models.ManyToManyField(Author, related_name='books')

#     def __str__(self):
#         return self.title


@pytest.mark.django_db  # type: ignore[attr-defined]  
def test_many_to_many():   # Тестируем ManyToMany
    law1 = Law.objects.create(
        title="Федеральный закон №59", shorttitle="59-ФЗ")
    law2 = Law.objects.create(
        title="Федеральный закон №147", shorttitle="147-ФЗ")
    category = Category.objects.create(title="Судебная практика")
    departament = Departament.objects.create(title="Канцелярия")
    status = Status.objects.create(title="Архив")
    user = User.objects.create(username='admin')
    document = Document.objects.create(
        user=user,
        category=category,
        title="Практика закона о торгавли",
        departament=departament,
        status=status,
        # date_create="29-01-2023",
        text="Тестовая страница с текстом.")
    document.law.add(law1, law2)
    print('!!!!!', law1, law2)
    assert document.user.username == "admin"
    assert document.title == "Практика закона о торгавли"
    # assert document.category == "Судебная практика"
    assert document.law == ("59-ФЗ", "147-ФЗ")
    assert document.departament.title == "Канцелярия"
    assert document.status.title == "Архив"
    assert document.text == "Тестовая страница с текстом."
    # book1 = Book.objects.create(title='Book 1')   # Создание книги 1
    # book2 = Book.objects.create(title='Book 2')   # Создание книги 2
    # book1.authors.add(author1, author2)  # Добавляем 2-х авторов
    # (author1, author2)к book1
    # book2.authors.add(author2)  # Добавляем 1-го (author2)к book2
    # assert book1 in author1.books and book1 in author2 .books and book2
    # in author2 .books



# @pytest.mark.django_db
# def test_document_creation():
#     user = User(1)
#     category = Category.objects.create(title="Судебная практика")
#     departament = Departament.objects.create(title="Канцелярия")
#     # law = Law.objects.create(title="Федеральный закон №59", shorttitle="59-ФЗ")
#     status = Status.objects.create(title="Архив")
#     document = Document.objects.create(
#         user=user,
#         category=category,
#         title="Практика закона о торгавли",
#         departament=departament,
#         status=status,
#         # date_create="29-01-2023",
#         text="Тестовая страница с текстом.")
        
#     print('!!!!!', document.departament)
#     assert document.title == "Практика закона о торгавли"
#     # assert document.category == "Судебная практика"
#     # assert document.law == ("Федеральный закон №59",)
#     assert document.departament.title == "Канцелярия"
#     assert document.status.title == "Архив"
#     assert document.text == "Тестовая страница с текстом."
#     # assert document.date_create == "29-01-2023"


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
