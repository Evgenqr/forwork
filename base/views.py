from audioop import reverse
from http.client import HTTPResponse
import json
from django.urls import reverse # type: ignore
from multiprocessing import context
from unicodedata import category
from django.contrib import messages # type: ignore
from django.shortcuts import redirect, render, get_object_or_404 # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.db import IntegrityError # type: ignore
from django.contrib.auth import login, logout, authenticate # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.views import View # type: ignore
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # type: ignore
from .models import Category, Document, Law, DocumentFile
from .forms import CategoryForm, DocumentForm, AuthForm
from django.utils.text import slugify # type: ignore
from transliterate import translit # type: ignore
import os
from django.db.models import Q # type: ignore
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage # type: ignore
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin # type: ignore
from django.http import JsonResponse # type: ignore


# ---- User
class LoginView(View):

    def post(self, request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(data={}, status=201)
            else:
                return JsonResponse(
                    data={'error': 'Пароль и/или логин не верны'},
                    status=400
                    )
        return JsonResponse(data={'error': 'Введите логин и пароль'}, status=400)
        # if user is None:
        #     return render(
        #         request, 'base/modal.html', {
        #             'form': AuthenticationForm(),
        #             'error': 'User or password did not match'
        #         })
        # else:
        #     login(request, user)
        #     return redirect(self.request.META.get('HTTP_REFERER', ''))


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

# ---- Home


def Home(request):
    return render(request, 'base/index.html')
# ---- END Home


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
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = Category.objects.all()
        context['laws'] = Law.objects.all()
        return context

    def get_queryset(self):
        slug = Category.objects.get(slug=self.kwargs['slug'])
        if slug:
            return Document.objects.filter(category=slug)

# ---- Category END

# ---- Document


class DocumentListView(ListView):
    model = Document
    template_name = 'base/index.html'
    context_object_name = 'documents_list'
    paginate_by = 5
    
    def get_queryset(self):
        return Document.objects.order_by('-date_create').select_related('category')

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        context['laws'] = Law.objects.all()
        context['category'] = Category.objects.all()
        return context


class LawListView(ListView):
    model = Document
    template_name = 'base/law_detail.html'
    context_object_name = 'documents'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super(LawListView, self).get_context_data(**kwargs)
        context['title'] = Law.objects.get(slug=self.kwargs['slug'])
        context['category'] = Category.objects.all()
        context['laws'] = Law.objects.all()
        return context

    def get_queryset(self):
        slug = Law.objects.get(slug=self.kwargs['slug'])
        if slug:
            return Document.objects.filter(law=slug).prefetch_related('category')
        # .prefetch_related('law')


FILE_EXT_WHITELIST = ['.pdf', '.txt', '.doc', '.docx', '.rtf',
                      '.xls', '.xlsx', '.ppt', '.pptx', '.png',
                      '.bmp', '.jpg', '.gif', '.zip', '.rar']


def check_lists(list_1,list_2): 
    return all(i in list_2 for i in list_1)


class DocumentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'base/createdocument.html'
    form_class = DocumentForm
    extra_context = {'documents': Document.objects.all()}
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(DocumentCreateView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['laws'] = Law.objects.all()
        return context

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
            return self.form_valid(form)
        else:
            ext_list = []
            for f in files:
                extension = os.path.splitext(f.name)[1]
                ext_list.append(extension)
            for f in files:
                if not all(i in FILE_EXT_WHITELIST for i in ext_list):
                    messages.add_message(request,
                                            messages.INFO,
                                            f'Выбранный файл не может быть загружен. Возможно загрузка файлов только со следующими расширениями: {FILE_EXT_WHITELIST}')
                    
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


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'base/document_detail.html'
    context_object_name = 'documents'


    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['laws'] = Law.objects.all()
        slug = self.kwargs.get('slug', '')
        context['slug'] = slug
        document = Document.objects.get(slug=slug)
        context['files'] = DocumentFile.objects.filter(document=document)
        return context


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    template_name = 'base/viewdocument.html'
    form_class = DocumentForm
    extra_context = {
        'documents': Document.objects.all(),
        'files': DocumentFile.objects.all()
        }
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(DocumentUpdateView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', '')
        document = Document.objects.get(slug=slug)
        context['files'] = DocumentFile.objects.filter(document=document)
        context['title'] = Document.objects.get(slug=self.kwargs['slug'])
        context['category'] = Category.objects.all()
        context['laws'] = Law.objects.all()
        # context['files'] = DocumentFile.objects.filter(
        #     document__slug=self.kwargs['slug'])
        return context

    def deletefile(self, request, pk):
        file = get_object_or_404(DocumentFile, pk=pk)
        slug = file.document.slug
        document = get_object_or_404(Document, slug=slug)
        if request.method == 'GET':
            file.delete()
            form = DocumentForm(instance=document)
            files = DocumentFile.objects.filter(document=document)
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        newfiles = self.request.FILES.getlist("files")
        document = get_object_or_404(Document, slug=self.kwargs['slug'])
        files = DocumentFile.objects.filter(document=document)
        laws = Law.objects.all()
        category = Category.objects.all()
        context = {
                        'document': document,
                        'files' :files,
                        'laws': laws,
                        'category':category, 
                        'form': form,
                    }
        if newfiles == []:
            try:
                form = DocumentForm(
                    request.POST, request.FILES, instance=document)
                form.save()
                return redirect('document_detail',  slug = document.slug)
            except ValueError:
                return render(request, self.template_name, {
                    'document': document,
                    'form': DocumentForm(),
                    'newfiles': newfiles,
                    'error': 'Bad info'
                })
        else:
            ext_list = []
            for f in newfiles:
                extension = os.path.splitext(f.name)[1]
                ext_list.append(extension)
            for f in newfiles:
                extension = os.path.splitext(f.name)[1]
                if not all(i in FILE_EXT_WHITELIST for i in ext_list):
                    # newfiles.remove(f)
                    messages.add_message(request,
                                         messages.INFO,
                                         f'Выбранный файл не может быть загружен. Возможно загрузка файлов только со следующими расширениями: {FILE_EXT_WHITELIST}')
                    return render(request, self.template_name, context)
                else:
                    form = DocumentForm(
                        request.POST, request.FILES, instance=document)
                    form.save()
                    DocumentFile.objects.create(
                        document=document, file=f)
                    form.save()
            return self.form_valid(form)
        
        
from django.http import JsonResponse
def deletefile(request):
    if request.user.is_authenticated() and request.is_ajax() and request.POST:
        object_id = request.POST.get('id', None)
        b = get_object_or_404(DocumentFile, id=object_id)
        b.delete()
        data = {'message': 'delete'.format(b)}
        return HTTPResponse(json.dumps(data), content_type='application/json')
    else:
        return JsonResponse({'error': 'Only authenticated users'}, status=404)

@login_required
def deletefile2(request, pk):
    file = get_object_or_404(DocumentFile, pk=pk)
    slug = file.document.slug
    document = get_object_or_404(Document, slug=slug)
    if request.method == 'GET':
        file.delete()
        form = DocumentForm(instance=document)
        files = DocumentFile.objects.filter(document=document)
        return render(request, 'base/viewdocument.html', {
            'document': document,
            'files': files,
            'form': form
        })
            # return render(request, 'base/viewdocument.html', {
            #     'document': document,
            #     'files': files,
            #     'form': form
            # })   
    

# def deletefile(request, pk):
#     file = get_object_or_404(DocumentFile, pk=pk)
#     slug = file.document.slug
#     document = get_object_or_404(Document, slug=slug)
#     if request.method == 'GET':
#         file.delete()
#         form = DocumentForm(instance=document)
#         files = DocumentFile.objects.filter(document=document)
#         return render(request, 'base/viewdocument.html', {
#             'document': document,
#             'files': files,
#             'form': form
#         })  

# class FileDelete(DeleteView):
#     model = DocumentFile
#     template_name = 'base/viewdocument.html'
#     success_url = '/'

#     def post(self, *args, **kwargs):
#         file =  Document.objects.get(pk=self.kwargs['pk'])
#         files = DocumentFile.objects.filter(document__slug=self.kwargs['slug'])
#       
#         file.delete()
#         return redirect(self.get_success_url(), pk = file.pk)

# @login_required
# def deletefile(request, pk):
#     files = DocumentFile.objects.filter(file__pk=pk)
#   
#     if request.method == "POST":
#        
#         file = get_object_or_404(DocumentFile, pk=pk)

#         # file.delete()
#         return redirect('/')
#     elif request.method == "GET":
#        
#         # return render(request, 'base/viewdocument.html')
#     else:
#        
#         return redirect('/')

@login_required
def deletefile(request, pk):
    file = get_object_or_404(DocumentFile, pk=pk)
    slug = file.document.slug
    document = get_object_or_404(Document, slug=slug)
    if request.method == 'GET':
        file.delete()
        form = DocumentForm(instance=document)
        files = DocumentFile.objects.filter(document=document)
        return render(request, 'base/viewdocument.html', {
            'document': document,
            'files': files,
            'form': form
        })


class DocumentDelete(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'base/viewdocument.html'
    success_url = '/'

    def delete(self, *args, **kwargs):
        document = Document.objects.get(slug=self.kwargs['slug'])
        document.delete()
        return redirect('home')


# @login_required
# def deletedocument(request, slug):
#     document = get_object_or_404(Document, slug=slug)
#     if request.method == 'POST':
#         document.delete()
#         
#         return redirect('home')
#     else:
#        
#         return redirect('home')

# def delete_task(request, file_id):
#     file = DocumentFile.objects.get(id=file_id)
#     file.objects.delete()

#     file = DocumentFile.objects.order_by('date_added')
#     context = {'file': file}
#     return render(request, 'work_list/index.html', context)


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


#  ---- Document END


class SearchView(ListView):
    model = Document
    template_name = 'base/search_result.html'
    paginate_by = 3
    
    def get(self, request, *args, **kwargs):
        context = {}
        q = request.GET.get('q')
        if q:
            query_sets = []  # Общий QuerySet
            query_sets.append(Document.objects.filter(
                Q(title__icontains=q) | Q(text__icontains=q)))
            final_set = list(chain(*query_sets))
            context['last_question'] = '?q=%s' % q
            current_page = Paginator(final_set, 10)
            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(
                    current_page.num_pages)

        context['category'] = Category.objects.all()
        context['laws'] = Law.objects.all()
        return render(request=request, template_name=self.template_name, context=context)
