from pydoc import Doc
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
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
from .models import Category, Document, Law, File
from .forms import CategoryForm, DocumentForm, FileForm
from django.utils.text import slugify
from transliterate import translit
# from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect


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
    # print('111ggg', Law.objects.all())

    #  def get_context_data(self, **kwargs):
    #     context = super(DocumentListView, self).get_context_data(**kwargs)
    #     context['title'] = Document.objects.get(slug=self.kwargs['slug'])
    #     return context

    # return render(request, 'base/index.html')


class DocumentCreate(CreateView):
    model = DocumentForm
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
        else:
            return self.form_invalid(form)




@login_required
def createdocument(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdocument = form.save(commit=False)
            # file = request.FILES.getlist('file')[0]
            
            # newdocument = Document.objects.create(file=file)
            # newdocument.save()
            newdocument.user = request.user
            newdocument.slug = translit(newdocument.title,
                                        language_code='ru',
                                        reversed=True)
            newdocument.slug = slugify(newdocument.slug)
            newdocument.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'base/createdocument.html', {'form': form})


@login_required
def createdocumen2t(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():

            # category = form.cleaned_data.get('category')
            newdocument = form.save(commit=False)
            newdocument.user = request.user
            newdocument.slug = translit(newdocument.title,
                                        language_code='ru',
                                        reversed=True)
            newdocument.slug = slugify(newdocument.slug)
            newdocument.save()
            # for cat in category:
            #     newidocument.category.add(cat)
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'base/createdocument.html', {'form': form})


def document_detail_view(request, slug):
    document = get_object_or_404(Document, slug=slug)
    # files = File.objects.filter(document=document)
    laws = Law.objects.filter(document=document)
    context = {
        'document': document,
        # 'files': files,
        'laws': laws
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
