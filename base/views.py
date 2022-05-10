# from pydoc import Doc
from django.views.generic.edit import FormView
from django.views.generic import CreateView
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
# from django.views.generic.edit import FormView
# from django.http import HttpResponse
# from django.db.models import Q
# from django.views import View
# from itertools import chain
from .models import Category, Document, Law, DocumentFile
from .forms import CategoryForm, DocumentForm
from django.utils.text import slugify
from transliterate import translit
# from django.views.generic.edit import FormView


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
                'error': 'Bad data passed in'
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
                    'error': 'Bad info'
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
# class DocumentViews(ListView):
#     model = Document
#     template_name = 'base/document_detail.html'
#     context_object_name = 'documents'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = Document.objects.get(slug=self.kwargs['slug'])
    #     return context

    # def get_queryset(self):
    #     slug = Document.objects.get(slug=self.kwargs['slug'])
    #     if slug:
    #         return Item.objects.filter(monster=slug)

class DocumentListView(ListView):
    template_name = 'base/index.html'
    context_object_name = 'documents_list'

    def get_queryset(self):
        return Document.objects.order_by('date_create')

    # def get_context_data(self, **kwargs):
    #     context = super(DocumentListView, self).get_context_data(**kwargs)
    #     context['title'] = Document.objects.get(slug=self.kwargs['slug'])
    #     return context


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
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        newdocument = form.save(commit=False)
        newdocument.user = request.user
        print('ss111sss', newdocument.user)
        newdocument.slug = translit(newdocument.title,
                                    language_code='ru',
                                    reversed=True)
        newdocument.slug = slugify(newdocument.slug)
        newdocument.save()
        files = self.request.FILES.getlist("files")
        for f in files:
            DocumentFile.objects.create(
                document=newdocument, file=f)
        return self.form_valid(form)

    # def form_valid(self, form):
    #     newdocument = form.save()
    #     newdocument.user = "admin"
    #     newdocument.slug = translit(newdocument.title,
    #                                 language_code='ru',
    #                                 reversed=True)
    #     newdocument.slug = slugify(newdocument.slug)
    #     newdocument.save()
    #     files = self.request.FILES.getlist("files")
    #     for f in files:
    #         DocumentFile.objects.create(document=newdocument, file=f)
    #     return super().form_valid(form)


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
#     def post(self, request, *args, **kwargs):
#         form_class = DocumentForm
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('files')
#         if form.is_valid():
#             print('bbb')
#             newdocument = form.save(commit=False)
#             newdocument.user = request.user
#             newdocument.slug = translit(newdocument.title,
#                                         language_code='ru',
#                                         reversed=True)
#             newdocument.slug = slugify(newdocument.slug)
#             newdocument.save()
#             k = 0
#             # for f in files:
#             #     k += 1
#             #     print('f', f)
#             #     Document.objects.create(slug=newdocument.slug,
#             #                             file=f, category=newdocument.category,
#             #                             user=newdocument.user)
#             #     print('bbb')

#             print('ss111sss', k)
#             return self.form_valid(form)
#         else:
#             print('sssss')
#             return self.form_invalid(form)


# class DocumentCreate(CreateView):
#     model = Document
#     # form_class = DocumentForm
#     # extra_context = {'documents': Document.objects.all()}
#     template_name = 'base/createdocument.html'
#     success_url = '/'

#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         # form_class = DocumentForm(request.POST, request.FILES)
#         form = self.get_form(form_class)
#         if form.is_valid():
#             newdocument = form.save(commit=False)
#             newdocument.user = request.user
#             newdocument.slug = translit(newdocument.title,
#                                         language_code='ru',
#                                         reversed=True)
#             newdocument.slug = slugify(newdocument.slug)
#             newdocument.save()
#         else:
#             return self.form_invalid(form)


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


class DocumentView(DetailView):
    model = Document
    template_name = 'base/document_detail.html'
    # slug_url_kwarg = 'documents_slug'
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
