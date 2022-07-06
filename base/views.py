from audioop import reverse
from http.client import HTTPResponse
import json
import re
from urllib import request
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
from .models import Category, Document, Law, DocumentFile, Departament, Status
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
class CategoryListView(ListView):

    model = Document
    template_name = 'base/category_detail.html'
    context_object_name = 'documents'
    paginate_by = 3
    
    def get_queryset(self):
        self.cat = Category.objects.get(slug=self.kwargs['slug'])
        slug =  self.cat
        if slug:
            return Document.objects.filter(category=slug)
        
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(*kwargs)
        context['title'] =  self.cat
        return context
# ---- Category END


# ---- Departamen
class DepartamentListView(ListView):
    model = Document
    template_name = 'base/departament_detail.html'
    context_object_name = 'documents'
    paginate_by = 3
    
    def get_queryset(self):
        self.dep = Departament.objects.get(slug=self.kwargs['slug'])
        slug = self.dep
        if slug:
            return Document.objects.filter(departament=slug)    
        
    def get_context_data(self, **kwargs):
        context = super(DepartamentListView, self).get_context_data(**kwargs)
        context['title'] = self.dep
        return context
# ---- Departamen END


# ---- Status
class StatusListView(ListView):
    model = Document
    template_name = 'base/status_detail.html'
    context_object_name = 'documents'
    paginate_by = 3
    
    def get_queryset(self):
        self.sts = Status.objects.get(slug=self.kwargs['slug'])
        slug = self.sts 
        if slug:
            return Document.objects.filter(status=slug)
        
    def get_context_data(self, **kwargs):
        context = super(StatusListView, self).get_context_data(**kwargs)
        context['title'] = self.sts 
        return context
# ---- Status END


# ---- Law
class LawListView(ListView):
    model = Document
    template_name = 'base/law_detail.html'
    context_object_name = 'documents'
    paginate_by = 3
    
    def get_queryset(self):
        self.law = Law.objects.get(slug=self.kwargs['slug'])
        slug = self.law
        if slug:
            return Document.objects.filter(law=slug).prefetch_related('category')
        # .prefetch_related('law')
        
    def get_context_data(self, **kwargs):
        context = super(LawListView, self).get_context_data(**kwargs)
        context['title'] = self.law
        return context
# ---- Law END
    
    
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
        return context


FILE_EXT_WHITELIST = ['.pdf', '.txt', '.doc', '.docx', '.rtf',
                      '.xls', '.xlsx', '.ppt', '.pptx', '.png',
                      '.bmp', '.jpg', '.gif', '.zip', '.rar']


class DocumentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'base/createdocument.html'
    form_class = DocumentForm
    extra_context = {'documents': Document.objects.all()}
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super(DocumentCreateView, self).get_context_data(**kwargs)
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
        context['title'] = self.document
        context['files'] = DocumentFile.objects.filter(document=self.document)
        return context
    
    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', '')
        context['slug'] = slug
        document = Document.objects.get(slug=slug)
        context['files'] = DocumentFile.objects.filter(document=document)
        return context

from django.http import HttpResponse


@login_required
def deleteitems(request):
    # newdata = request.user
    # profiledata = User.objects.get(user=newdata)
    swid = request.POST.getlist('newval[]') # ajax post data (which have all id of GalleryImage objects)
    for one in swid:
        obj = DocumentFile.objects.get(id=one) #.delete()
        print('----', obj)
    response = json.dumps({'data':'deleted'})
    return HttpResponse(response, mimetype="application/json")


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    template_name = 'base/viewdocument.html'
    form_class = DocumentForm
    # extra_context = {
    #     'documents': Document.objects.all(),
    #     'files': DocumentFile.objects.all()
    #     }
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(DocumentUpdateView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', '')
        document = Document.objects.get(slug=slug)
        context['files'] = DocumentFile.objects.filter(document=document)
        context['title'] = Document.objects.get(slug=self.kwargs['slug'])
        return context
    
    # def file_for_delete(self, request, *args, **kwargs):
    #     if request.method == 'POST' and request.is_ajax():
    #         print('bgbg')
    #         return HttpResponse('ok')
    #     else:
    #         print('nooo')
    #         return HttpResponse('bad')
    
    def post(self, request, *args, **kwargs):
        # if request.is_ajax():

            # return HttpResponse('ok')
        # else:
        #     print('nooo')
            # return HttpResponse('bad')
        # arr_of_id1 = request.GET.get('arr_of_id[]')
        # print('3331', arr_of_id1)
        
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        newfiles = self.request.FILES.getlist("files")
        document = get_object_or_404(Document, slug=self.kwargs['slug'])
        files = DocumentFile.objects.filter(document=document)
        context = {
                        'document': document,
                        'files' :files,
                        'form': form,
                    }
        if newfiles == []:
           
            try:
                # arr_of_id2 = request.GET.getlist('arr_of_id[]')

                
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
  
# def testajax(request): 
#     data = 'fff'
#     # if request.GET:
#     data = request.GET.get('data')
#     return JsonResponse({
#             'data': data,
#         })


def testajax(request):
    # data = 'ds'
    # data2 = 'gg'  
    # if request.GET:
    data = request.POST.get("data")
    data2 = request.GET.get("data")
    # data2 = '34' + data
    print('================ ', data)
    print('333 ', data2)
    return JsonResponse({
            'data': data,
            'data2': data2,
        })
    
    
class DocumentDelete(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'base/viewdocument.html'
    success_url = '/'

    def delete(self, *args, **kwargs):
        document = Document.objects.get(slug=self.kwargs['slug'])
        document.delete()
        return redirect('home')       
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



# def deletefile(request):
#     form = DocumentForm
#     print('1111')
    # if request.user.is_authenticated() and request.is_ajax():
    #     form = DocumentForm(request.POST)
    #     if form.is_valid():
    #         data = {'file': form.cleaned_data['files']}
    #         return JsonResponse({'good': data})
    # else:
    #     return JsonResponse({'error': 'Only authenticated users'}, status=404)


# ++
# @login_required
# def deletefile(request, pk):
#     file = get_object_or_404(DocumentFile, pk=pk)
#     slug = file.document.slug
#     print('!!!!!!file', file.pk)
#     document = get_object_or_404(Document, slug=slug)
#     if request.method == 'GET':
#         # file.delete()
#         form = DocumentForm(instance=document)
#         # files = DocumentFile.objects.filter(document=document)
#         return render(request, 'base/viewdocument.html', {
#             'document': document,
#             'file': file,
#             'form': form
#         })
        
        
        
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

# @login_required
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
