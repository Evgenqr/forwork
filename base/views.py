from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Category, Document, Law, DocumentFile, Departament, Status
from .forms import DocumentForm
import os
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime


# ---- User
class LoginView(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse(data={}, status=201)
            else:
                return JsonResponse(
                    data={'error': 'Пароль и/или логин не верны'},
                    status=400)
        return (
            JsonResponse(data={'error': 'Введите логин и пароль'}, status=400)
        )


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
    paginate_by = 10

    def get_queryset(self):
        self.cat = Category.objects.get(slug=self.kwargs['slug'])
        slug = self.cat
        if slug:
            return Document.objects.filter(category=slug)

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(*kwargs)
        context['title'] = self.cat
        return context
# ---- Category END


# ---- Departamen
class DepartamentListView(ListView):
    model = Document
    template_name = 'base/departament_detail.html'
    context_object_name = 'documents'
    paginate_by = 10

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
    paginate_by = 10

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
    paginate_by = 10

    def get_queryset(self):
        self.law = Law.objects.get(slug=self.kwargs['slug'])
        slug = self.law
        if slug:
            return (
                Document.objects.filter(law=slug).prefetch_related('category')
            )

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
    paginate_by = 10

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
        slug = self.kwargs.get('slug', '')
        context['slug'] = slug
        document = Document.objects.get(slug=slug)
        context['files'] = DocumentFile.objects.filter(document=document)
        return context


class DocumentUpdateView(LoginRequiredMixin, UpdateView):
    model = Document
    template_name = 'base/viewdocument.html'
    form_class = DocumentForm
    template_name_suffix = '_update'

    def get_context_data(self, **kwargs):
        context = super(DocumentUpdateView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug', '')
        document = Document.objects.get(slug=slug)
        context['files'] = DocumentFile.objects.filter(document=document)
        context['title'] = Document.objects.get(slug=self.kwargs['slug'])
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        newfiles = self.request.FILES.getlist("files")
        document = get_object_or_404(Document, slug=self.kwargs['slug'])
        files = DocumentFile.objects.filter(document=document)
        context = {
            'document': document,
            'files': files,
            'form': form
        }

        # --------------------------------
        if request.is_ajax():
            arr_of_id = request.POST.getlist("arr_of_id[]")
            for f_id in arr_of_id:
                file = get_object_or_404(DocumentFile, pk=f_id)
                slug = file.document.slug
                document = get_object_or_404(Document, slug=slug)
                file.delete()
        # ---------------------------------
        if newfiles == []:
            try:
                form = DocumentForm(
                    request.POST, request.FILES, instance=document)
                form.save()
                return redirect('document_detail', slug=document.slug)
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

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(DocumentUpdateView, self).dispatch(*args, **kwargs)


class DocumentDelete(LoginRequiredMixin, DeleteView):
    model = Document
    template_name = 'base/viewdocument.html'
    success_url = '/'

    def delete(self, *args, **kwargs):
        document = Document.objects.get(slug=self.kwargs['slug'])
        document.delete()
        return redirect('home')
#  ---- Document END


class DocumentFilter:

    def get_category(self):
        return Category.objects.all()


class ExtSearch(ListView):
    model = Document
    template_name = 'base/ext_search.html'
    form_class = DocumentForm
    extra_context = {'documents': Document.objects.all()}
    # success_url = 'base/search_result.html'
    paginate_by = 10

    def get_queryset(self):
        category = self.request.GET.getlist("category")
        departament = self.request.GET.getlist("departament")
        status = self.request.GET.getlist("status")
        law = self.request.GET.getlist("law")
        startdate = datetime.date.today()
        enddate = datetime.date.today()
        startdate = self.request.GET.get("startdate")
        enddate = self.request.GET.get("enddate")
        if startdate == "":
            startdate = "2000-01-01"
        if enddate == "":
            enddate = datetime.date.today()
        if category == []:
            category = Category.objects.all()
        if departament == []:
            departament = Departament.objects.all()
        if status == []:
            status = Status.objects.all()
        if law == []:
            law = Law.objects.all()
        queryset = Document.objects.filter(
            Q(category__in=category),
            Q(departament__in=departament),
            Q(status__in=status),
            Q(date_create__range=[startdate, enddate]),
            Q(law__in=law)
        )
        return queryset

    # def get(self, request):
    #     tasks = Document.objects.all()
    #     paginator = Paginator(tasks, 100)
    #     page_number = self.request.GET.get('page', 1)
    #     page = paginator.get_page(page_number)
    #     count = tasks.count()
    #     type = 'Все задачи'
    #     return render(request, 'base/ext_search.html',
    # context={'tasks': page, 'count': count, 'type': type,})


class SearchView(ListView):
    # model = Document
    template_name = 'base/search_result.html'
    # form_class = DocumentForm
    # paginate_by = 10

    def get(self, request, *args, **kwargs):
        context = {}
        q = request.GET.get('q')
        if q:
            # query_sets = []  # Общий QuerySet
            document_list = Document.objects.filter(
                Q(title__icontains=q) | Q(text__icontains=q))
            category_list = Document.objects.filter(
                Q(category__title__icontains=q))
            departament_list = Document.objects.filter(
                Q(departament__title__icontains=q))
            law_list = Document.objects.filter(Q(law__title__icontains=q))
            status_list = Document.objects.filter(
                Q(status__title__icontains=q))
            final_set = list(chain(document_list, category_list,
                             departament_list, law_list, status_list))
            context['last_question'] = '?q=%s' % q
            current_page = Paginator(final_set, 100)
            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(
                    current_page.num_pages)
        return render(
            request=request,
            template_name=self.template_name,
            context=context
        )
