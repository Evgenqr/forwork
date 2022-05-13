from pickle import NONE
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
# from django.db.models import Q
from .models import Category, Document, Law, DocumentFile
from .forms import CategoryForm, DocumentForm
from django.utils.text import slugify
from transliterate import translit
import os


# ---- User
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'base/signupuser.html',
                      {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/')
            except IntegrityError:
                return render(
                    request, 'base/signupuser.html', {
                        'form': UserCreationForm(),
                        'error': 'That username has already been taken'
                    })
        else:
            return render(request, 'base/signupuser.html', {
                'form': UserCreationForm(),
                'error': 'Password did not match'
            })


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'base/loginuser.html',
                      {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is None:
            return render(
                request, 'base/loginuser.html', {
                    'form': AuthenticationForm(),
                    'error': 'User or password did not match'
                })
        else:
            login(request, user)
            return redirect('/')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
# ---- User END

# ---- ?????


def Home(request):
    return render(request, 'base/index.html')


def Fas(request):
    return render(request, 'base/fas.html')
# ---- ?????


# ---- Category
@login_required
def createcategory(request):
    if request.method == 'GET':
        return render(request, 'base/createcategory.html',
                      {'form': CategoryForm()})
    else:
        try:
            form = CategoryForm(request.POST, request.FILES)
            newcategory = form.save(commit=False)
            # newlocaltion.slug = request.user
            newcategory.user = request.user
            newcategory.slug = translit(newcategory.title,
                                        language_code='ru',
                                        reversed=True)
            newcategory.slug = slugify(newcategory.slug)
            newcategory.save()
            return redirect('home')
        except ValueError:
            return render(request, 'base/createcategory.html', {
                'form': CategoryForm(),
                'error': 'Ошибка ввода данных'
            })


@login_required
def viewcategory(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'GET':
        form = CategoryForm(instance=category)
        return render(request, 'base/viewcategory.html', {
            'category': category,
            'form': form
        })
    else:
        try:
            form = CategoryForm(request.POST,
                                request.FILES,
                                instance=category)
            form.save()
            return redirect('home')
        except ValueError:
            return render(
                request, 'base/viewcategory.html', {
                    'category': category,
                    'form': CategoryForm(),
                    'error': 'Ошибка ввода данных'
                })


@login_required
def deletecategory(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        return redirect('/')
    return redirect('/')
# ---- Category END


# ---- Document

class DocumentListView(ListView):
    template_name = 'base/index.html'
    context_object_name = 'documents_list'

    def get_queryset(self):
        return Document.objects.order_by('date_create')

    # def get_context_data(self, **kwargs):
    #     context = super(DocumentListView, self).get_context_data(**kwargs)
    #     context['title'] = Document.objects.get(slug=self.kwargs['slug'])
    #     return context


class LawDetailListView(ListView):
    template_name = 'base/lawdetail.html'
    context_object_name = 'law_list'

    def get_queryset(self):

        return Document.objects.filter('date_create')

    # def get_context_data(self, **kwargs):
    #     context = super(DocumentListView, self).get_context_data(**kwargs)
    #     context['title'] = Document.objects.get(slug=self.kwargs['slug'])
    #     return context


def law_detail_view(request, slug):
    law = get_object_or_404(Law, slug=slug)
    print('law ', law)
    documents = Document.objects.filter(law=law)
    print('!!!!!!!!!!', documents)
    context = {
        'law': law,
        'documents': documents,
    }
    return render(request, 'base/lawdetail.html', context)


class LawListView(ListView):
    # model = Law
    # template_name = 'incude/header.html'
    template_name = 'base/index.html'
    context_object_name = 'laws'

    def get_queryset(self):
        return Law.objects.order_by('title')


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/login/")
        return super().dispatch(request, *args, **kwargs)


class DocumentCreateView(CreateView):
    template_name = 'base/createdocument.html'
    form_class = DocumentForm
    extra_context = {'documents': Document.objects.all()}
    success_url = '/'

    def post(self, request, *args, **kwargs):
        FILE_EXT_WHITELIST = ['.pdf', '.txt', '.doc', '.docx', '.rtf',
                              '.xls', '.xlsx', '.ppt', '.pptx', '.png',
                              '.jpg', '.gif', '.zip', '.rar', '.txt']
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = self.request.FILES.getlist("files")
        print('554', files)
        if files == []:
            print('!!!----')
            newdocument = form.save(commit=False)
            newdocument.user = request.user
            newdocument.slug = translit(newdocument.title,
                                        language_code='ru',
                                        reversed=True)
            newdocument.slug = slugify(newdocument.slug)
            newdocument.save()
            DocumentFile.objects.create(
                document=newdocument, file=False)
            return self.form_valid(form)
        else:
            for f in files:
                extension = os.path.splitext(f.name)[1]
                print('vvvvddsv', f)
                if extension not in FILE_EXT_WHITELIST:
                    files.remove(f)
                    print('dds', extension)
                    messages.add_message(request,
                                         messages.INFO,
                                         'Выбранный файл не может быть загружен. Возможно загрузка файлов только со следующими расширениями: txt, doc, docx, xls, xlsx, pdf, png, jpg, rar, zip, ppt, pptx, rtf, gif.')
                    form = form
                    return render(request, self.template_name, {'form': form})
                else:
                    newdocument = form.save(commit=False)
                    newdocument.user = request.user
                    newdocument.slug = translit(newdocument.title,
                                                language_code='ru',
                                                reversed=True)
                    newdocument.slug = slugify(newdocument.slug)
                    newdocument.save()
                    DocumentFile.objects.create(
                        document=newdocument, file=f)
            return self.form_valid(form)


class DocumentCreate(FormView):
    form_class = DocumentForm
    extra_context = {'documents': Document.objects.all()}
    template_name = 'base/createdocument.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            newdocument = form.save(commit=False)
            newdocument.user = request.user
            newdocument.slug = translit(newdocument.title,
                                        language_code='ru',
                                        reversed=True)
            newdocument.slug = slugify(newdocument.slug)
            newdocument.save()
            print('ss111sss')
            return self.form_valid(form)
        else:
            print('sssss')
            return self.form_invalid(form)


def document_detail_view(request, slug):
    document = get_object_or_404(Document, slug=slug)
    files = DocumentFile.objects.filter(document=document)
    laws = Law.objects.filter(document=document)
    context = {
        'document': document,
        'laws': laws,
        'files': files
    }
    return render(request, 'base/document_detail.html', context)


def document_detail_view1(request, slug):
    document = get_object_or_404(Document, slug=slug)
    files = DocumentFile.objects.filter(document=document)
    print('0000000', bool(files))
    laws = Law.objects.filter(document=document)
    if list(files) == None:
        print('????????????????')
        context = {
            'document': document,
            'laws': laws,
        }
    else:
        print('iiiiiiiiiiiiiiiiii')
        context = {
            'document': document,
            'laws': laws,
            'files': files
        }
    return render(request, 'base/document_detail.html', context)


class DocumentView(DetailView):
    model = Document
    template_name = 'base/document_detail.html'
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Document.objects.get(slug=self.kwargs['slug'])
        # context['law'] = Law.objects.get(slug=self.kwargs['slug'])
        return context


@login_required
def viewdocument(request, slug):
    document = get_object_or_404(Document, slug=slug)
    if document.user == request.user:
        #  or request.user.has_perm('auth.change_user')
        if request.method == 'GET':
            form = DocumentForm(instance=document)
            return render(request, 'base/viewdocument.html', {
                'document': document,
                'form': form
            })
        else:
            try:
                form = DocumentForm(
                    request.POST, request.FILES, instance=document)
                form.save()
                return redirect('home')
            except ValueError:
                return render(request, 'base/viewdocument.html', {
                    'document': document,
                    'form': DocumentForm(),
                    'error': 'Bad info'
                })
    else:
        return redirect('/')


@login_required
def deletedocument(request, slug):
    document = get_object_or_404(Document, slug=slug)
    if document.user == request.user:
        #  or request.user.has_perm('auth.change_user')
        if request.method == 'POST':
            document.delete()
            return redirect('home')
    else:
        return redirect('/')
# ---- Document END


class CourtsView(ListView):
    model = Document
    template_name = 'base/courts.html'
    context_object_name = 'courts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Document.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        slug = Document.objects.get(slug=self.kwargs['slug'])
        if slug:
            return Document.objects.filter(category=slug)
