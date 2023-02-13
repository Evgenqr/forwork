from base.models import Status, Departament, Law, Category, Document
from django.contrib.auth.models import User


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
