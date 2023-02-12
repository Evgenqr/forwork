from base.forms import AuthForm
from base.models import (
    Category, Departament, Status, Law, Document, DocumentFile)


def get_context_data(request):
    context = {
        'login_form': AuthForm(),
        'category': Category.objects.all(),
        'departament': Departament.objects.all(),
        'status': Status.objects.all(),
        'laws': Law.objects.all(),
        'documents': Document.objects.all(),
        'files': DocumentFile.objects.all()
    }
    return context
