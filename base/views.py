from unicodedata import category
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
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


# def Fas(request):
#     return render(request, 'base/fas.html')
# ---- ?????


# ---- Category
@login_required
def createcategory(request):
    category = Category.objects.all()
    laws = Law.objects.all()
    
    if request.method == 'GET':
        return render(request, 'base/createcategory.html', {
                'form': CategoryForm(),
                'category': category,
                'laws': laws, 
            })
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
                'category': category,
                'laws': laws, 
                'error': 'Ошибка ввода данных'
            })

class CategoryListView(ListView):
    model = Document
    template_name = 'base/category_detail.html'
    context_object_name = 'documents'
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = Category.objects.all()
        context['laws'] = Law.objects.all()
        # context['documents'] = Document.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        slug = Category.objects.get(slug=self.kwargs['slug'])
        if slug:
            return Document.objects.filter(category=slug)

# def category_detail_view(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     documents = Document.objects.filter(category=category)

#     context = {
#         'category': category,
#         'documents': documents,
#     }
#     return render(request, 'base/category_detail.html', context)


# @login_required
# def viewcategory(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     categories = Category.objects.all()
#     laws = Law.objects.all()
#     if request.method == 'GET':
#         form = CategoryForm(instance=category)
#         return render(request, 'base/viewcategory.html', {
#             'category': category,
#             'laws': laws,
#             'categories': categories,
#             'form': form
#         })
#     else:
#         try:
#             form = CategoryForm(request.POST,
#                                 request.FILES,
#                                 instance=category)
#             form.save()
#             return redirect('home')
#         except ValueError:
#             return render(
#                 request, 'base/viewcategory.html', {
#                     'category': category,
#                     'laws': laws,
#                     'categories': categories,
#                     'form': CategoryForm(),
#                     'error': 'Ошибка ввода данных'
#                 })


# @login_required
# def deletecategory(request, slug):
#     category = get_object_or_404(Category, slug=slug)
#     if request.method == 'POST':
#         category.delete()
#         return redirect('/')
#     return redirect('/')
# ---- Category END

def document_list(request):
    law = Law.objects.all()
    category = Category.objects.all()
    context = {
        'category': category,
        'law': law,
    }
    return render(request, 'include/header.html', context)
# ---- Document

class DocumentListView(ListView):
    model = Document
    template_name = 'base/index.html'
    context_object_name = 'documents_list'

    def get_queryset(self):
        # slug = Document.objects.get(slug=self.kwargs['slug'])
        # if slug:
        return Document.objects.order_by('date_create')

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        # context['title'] = Document.objects.get(slug=self.kwargs['slug'])
        context['laws'] =Law.objects.all()
        context['category'] = Category.objects.all()
        return context


class LawListView(ListView):
    model = Document
    template_name = 'base/law_detail.html'
    context_object_name = 'documents'
    def get_context_data(self, **kwargs):
        context = super(LawListView, self).get_context_data(**kwargs)
        context['title'] = Law.objects.get(slug=self.kwargs['slug'])
        context['category'] = Category.objects.all()
        context['laws'] =Law.objects.all()
        # context['documents'] = Document.objects.get(slug=self.kwargs['slug'])
        
        return context

    def get_queryset(self):
        slug = Law.objects.get(slug=self.kwargs['slug'])
        if slug:
            return Document.objects.filter(law=slug)


# def law_detail_view(request, slug):
#     law = get_object_or_404(Law, slug=slug)
#     documents = Document.objects.filter(law=law)
#     context = {
#         'law': law,
#         'documents': documents,
#     }
#     return render(request, 'base/law_detail.html', context)


# class AdminRequiredMixin(object):
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             pass
#         else:
#             return redirect("/login/")
#         return super().dispatch(request, *args, **kwargs)

FILE_EXT_WHITELIST = ['.pdf', '.txt', '.doc', '.docx', '.rtf',
                        '.xls', '.xlsx', '.ppt', '.pptx', '.png',
                        '.jpg', '.bmp' '.gif', '.zip', '.rar', '.txt']


class DocumentCreateView(CreateView):
    template_name = 'base/createdocument.html'
    form_class = DocumentForm
    extra_context = {'documents': Document.objects.all()}
    success_url = '/'

    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = self.request.FILES.getlist("files")
        if files == []:
            newdocument = form.save(commit=False)
            newdocument.user = request.user
            newdocument.slug = translit(newdocument.title,
                                        language_code='ru',
                                        reversed=True)
            newdocument.slug = slugify(newdocument.slug)
            newdocument.save()
            # DocumentFile.objects.create(
            #     document=newdocument)
            return self.form_valid(form)
        else:
            for f in files:
                extension = os.path.splitext(f.name)[1]
                print('vvvvddsv', f)
                if extension not in FILE_EXT_WHITELIST:
                    files.remove(f)
                    print('noooooo', extension)
                    messages.add_message(request,
                                         messages.INFO,
                                         'Выбранный файл не может быть загружен. Возможно загрузка файлов только со следующими расширениями: txt, doc, docx, xls, xlsx, pdf, png, jpg, rar, zip, ppt, pptx, rtf, gif.')
                    form = form
                    return render(request, self.template_name, {'form': form})
                else:
                    print('eeeeeeeeeee')
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

    def get_context_data(self, **kwargs):
        context = super(DocumentCreateView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['laws'] =Law.objects.all()
        return context


# def document_detail_view(request, slug):
#     document = get_object_or_404(Document, slug=slug)
#     category = Category.objects.all()
#     files = DocumentFile.objects.filter(document=document)
#     laws = Law.objects.filter(document=document)
#     context = {
#         'document': document,
#         'category': category,
#         'laws': laws,
#         'files': files
#     }
#     return render(request, 'base/document_detail.html', context)


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'base/document_detail.html'
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['laws'] = Law.objects.all()
        slug = self.kwargs.get('slug', '')
        document = Document.objects.get(slug=slug)
        context['files']  = DocumentFile.objects.filter(document=document)
        return context


class DocumentUpdateView(UpdateView):
    model = Document
    template_name = 'base/viewdocument.html'
    form_class = DocumentForm
    extra_context = {'documents': Document.objects.all()}
    success_url = '/'
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(DocumentUpdateView, self).get_context_data(**kwargs)
        context['title'] = Document.objects.get(slug=self.kwargs['slug'])
        context['category'] = Category.objects.all()
        context['laws'] = Law.objects.all()
        # context['documents'] = Document.objects.get(slug=self.kwargs['slug'])
        
        return context


@login_required
def viewdocument(request, slug):
    document = get_object_or_404(Document, slug=slug)
    files = DocumentFile.objects.filter(document=document)
    # newfiles = self.request.FILES.getlist("files")
    if request.user:
        #  or request.user.has_perm('auth.change_user')
        if request.method == 'GET':
            form = DocumentForm(instance=document)
            return render(request, 'base/viewdocument.html', {
                'document': document,
                'files': files,
                'form': form
            })
        else:
            if list(files) == []:
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
                for f in files:
                    files.add(f)
                    extension = os.path.splitext(f.file.name)[1]
                    if extension not in FILE_EXT_WHITELIST:
                        files.remove(f)
                        messages.add_message(request,
                                            messages.INFO,
                                            'Выбранный файл не может быть загружен. Возможно загрузка файлов только со следующими расширениями: txt, doc, docx, xls, xlsx, pdf, png, jpg, rar, zip, ppt, pptx, rtf, gif.')
                        form = form
                        return render(request, 'base/viewdocument.html', {'form': form})
                try:
                    form = DocumentForm(
                        request.POST, request.FILES, instance=document)
                    form.save()
                    return redirect('home')
                except ValueError:
                    return render(request, 'base/viewdocument.html', {
                        'document': document,
                        'form': DocumentForm(),
                        'files': files,
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
            return redirect('/')
    else:
        return redirect('/')


#  ---- Document END


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
